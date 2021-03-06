from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView

from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect, render

from django.views import generic

from django.conf import settings

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError

from friendship.models import Friend, FriendshipRequest

from .forms import AccountLoginForm, AccountChangePasswordForm, AccountEditForm, AccountCreateForm, FriendsSearchForm

from .models import Account


def test(request):
    return render(request, 'base.html')


class AccountLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация пользователя
    """
    template_name = 'account/login.html'
    form_class = AccountLoginForm
    authentication_form = None
    redirect_authenticated_user = True


class UserLogOutView(LogoutView):
    """
    Выход из авторизаванного аккаунта
    """
    template_name = 'account/logout.html'
    next_page = '/blog/posts'  # TODO Добавить главную страницу!


class AccountProfileView(generic.detail.DetailView):
    """
    Страница авторизированного пользователя
    """
    model = Account

    def get(self, request, *args, **kwargs):
        username = self.request.user.username
        account = Account.objects.get(username=username)
        return render(request, 'account/profile.html', {'account': account})


class PublicAccountView(generic.detail.DetailView):
    """
    Страницы всех пользоватлей PyConnect
    """

    def get(self, request, *args, **kwargs):
        print(kwargs)
        account = Account.objects.get(id=kwargs['id'])
        return render(request, 'account/profile.html', {'account': account})


def get_user_edit(request):
    """
    Изменение данных пользователя
    """
    if request.POST:
        user_edit_form = AccountEditForm(request.POST, request.FILES, instance=request.user)
        if user_edit_form.is_valid():
            user_edit_form.save()
            return redirect('account_system:profile')

    else:
        user_edit_form = AccountEditForm(instance=request.user)
    return render(request, 'account/settings.html', {'user_edit_form': user_edit_form})


class AccountRegisterView(generic.CreateView):
    """
    Регистрация нового аккаунта
    """
    form_class = AccountCreateForm
    context_object_name = 'account_register_form'
    template_name = 'account/register.html'
    success_url = 'login'


class AccountEditView(generic.UpdateView):
    """
    Страница редактирования информацию пользовательского аккаунта.
    """
    form_class = AccountEditForm


class AccountFriends(generic.DetailView):
    """
    Друзья пользователя
    """
    model = settings.AUTH_USER_MODEL
    template_name = 'account/friends.html'

    def get(self, request, *args, **kwargs):
        unfriends = Friend.objects.unread_requests(user=request.user)
        sent_requests = Friend.objects.sent_requests(user=request.user)
        friends_search_form = FriendsSearchForm
        account_friends = Friend.objects.friends(request.user)
        return render(request, 'account/friends.html', {'account_friends': account_friends,
                                                        'friends_search_form': friends_search_form,
                                                        'unfriends': unfriends,
                                                        'sent_requests': sent_requests,
                                                        })


class SearchFriendsView(generic.DetailView):
    model = Account
    template_name = 'account/search_friend.html'

    def get(self, request, *args, **kwargs):
        print(request.META["QUERY_STRING"][9::])
        try:
            account = Account.objects.get(username=request.META["QUERY_STRING"][9::])
            friends = ''
            if Friend.objects.are_friends(request.user, account):
                friends = 'Your fiend!'
            return render(request, 'account/search_friend.html', {'account': account, 'friends': friends})
        except self.model.DoesNotExist:
            return redirect('account_system:friends')


def add_friend(request, master_account_id) -> redirect:
    """
    Добавление в друзья пользователя
    """
    master_account_id = int(master_account_id)
    master_account = Account.objects.get(id=master_account_id)
    if request.user.id == master_account.id:
        print('\nslave account\n')
        """
        Дружба с самим собой
        """
        return redirect('account_system:friends')
    try:
        Friend.objects.add_friend(
            request.user,
            master_account
        )
    except AlreadyFriendsError:
        return redirect('account_system:friends')
    return redirect('account_system:friends')


def get_make_friendship(request, slave_user_id) -> redirect:
    """
    Master account подтверждает дружбу со slave user
    """
    from_user = Account.objects.get(id=int(slave_user_id))
    friend_request = FriendshipRequest.objects.get(to_user=request.user, from_user=from_user)
    friend_request.accept()
    return redirect('account_system:friends')


def get_delete_friendship(request: str, slave_user_id) -> redirect:
    """
    Удаление из друзей
    """
    slave_user = Account.objects.get(id=int(slave_user_id))
    Friend.objects.remove_friend(request.user, slave_user)
    return redirect('account_system:friends')


class AccountChangePasswordView(PasswordChangeView):
    """
    Смена пароля пользователя
    """
    template_name = 'account/account_change_password.html'
    form_class = AccountChangePasswordForm
    success_url = 'account_system:me'


