from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ReferralCode, ReferralInvitation
from django.utils import timezone

@receiver(post_save, sender=User)
def handle_referral_registration(sender, instance, created, **kwargs):
    if created:
        # Проверяем, есть ли реферальный код в сессии
        from django.core.exceptions import ObjectDoesNotExist
        try:
            from django.core.cache import cache
            ref_code = cache.get(f'referral_code_{instance.email}')
            if ref_code:
                try:
                    referral_code = ReferralCode.objects.get(code=ref_code)
                    # Обновляем статистику реферала
                    referral_code.total_referrals += 1
                    referral_code.total_bonus += 500  # Бонус за реферала
                    referral_code.save()
                    
                    # Отмечаем приглашение как использованное
                    invitation = ReferralInvitation.objects.get(
                        referrer=referral_code.user,
                        referred_email=instance.email
                    )
                    invitation.is_registered = True
                    invitation.save()
                    
                    # Очищаем реферальный код из кэша
                    cache.delete(f'referral_code_{instance.email}')
                except (ReferralCode.DoesNotExist, ReferralInvitation.DoesNotExist):
                    pass
        except ObjectDoesNotExist:
            pass 