from django.shortcuts import render_to_response
from models import *
import datetime

def ipban(f):
	def wrap(request, *args, **kwargs):
		ip, created = IP.objects.get_or_create(ip=request.META['REMOTE_ADDR'])
		if created:
			ip.time = datetime.datetime.now() + datetime.timedelta(0, 10, 0)
		ip.requests += 1
		ip.save()
		if ip.banned_for_life:
			return render_to_response('ipban.html', {
				'ip': ip,
			})
		max_requests = 10
		if ip.requests >= max_requests:
			if datetime.datetime.now() < ip.time:
				if ip.requests == max_requests:
					ip.ban_counter += 1
					ip.time = datetime.datetime.now() + datetime.timedelta(0, 10, 0)
					ip.save()
				return render_to_response('ipban.html', {
					'ip': ip,
				})
			else:
				ip.requests = 0
				ip.time = datetime.datetime.now() + datetime.timedelta(0, 10, 0)
				ip.save()
		return f(request, *args, **kwargs)
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap
