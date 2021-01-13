from rest_framework import mixins


class CreateUpdateDestroy(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          ):
    pass


class ListRetrieveMixins(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin
                         ):
    pass