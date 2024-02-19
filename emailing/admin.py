from django.contrib import admin

from emailing.models import MailingList, Subscriber, Message


class MailingListAdmin(admin.ModelAdmin):
    pass


class SubscriberAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(MailingList, MailingListAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Message, MessageAdmin)
