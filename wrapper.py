from django.http import HttpResponse
from models import *
import datetime

def ipban(f):
	def wrap(request, *args, **kwargs):
		ip, created = IP.objects.get_or_create(ip=request.META['REMOTE_ADDR'])
		if created:
            # 10 Seconds span
			ip.time = datetime.datetime.now() + datetime.timedelta(0, 10, 0)
		ip.requests += 1
		ip.save()
		if ip.banned_for_life:
            return HttpResponse('You have been blocked for life!')
        # Maximum 10 requests allowed
		max_requests = 10
		if ip.requests >= max_requests:
			if datetime.datetime.now() < ip.time:
                # Too many requests in soo little time
                ip.ban_counter += 1
                # 10 Seconds span
                ip.time = datetime.datetime.now() + datetime.timedelta(0, 10, 0)
                ip.save()
                return HttpResponse('You have been blocked for 10 seconds!')
			else:
                # Reset the ip
				ip.requests = 0
                # 10 Seconds span
				ip.time = datetime.datetime.now() + datetime.timedelta(0, 10, 0)
				ip.save()
		return f(request, *args, **kwargs)
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap
