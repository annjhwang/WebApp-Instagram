from django.http import HttpResponse
from django.template import loader, Context
from django.shortcuts import render
from webapp.models import Image
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from django.shortcuts import render_to_response
from django.template import RequestContext

from el_pagination.decorators import page_template

import pprint
import requests
import datetime
import json
import os
import urllib
import urllib2


def search_form(request):
	return render(request, 'webapp/search_form.html')

API_PREFIX = 'https://api.instagram.com/v1'
CLIENT_ID = '4b88dab32ecd408e8060b8e1456b48c8'
ACCESS_TOKEN = '17599524.4b88dab.4304c5d135d9469aba6f1c363223feb6'

def make_api_request(url=None):
		"""Returns the dictionary from an API request."""
		# make an ajax get request
		request = urllib2.Request(url)
		f = urllib2.urlopen(request)
		response = f.read()
		f.close()
		# get and return desired data
		api_dict = json.loads(response)
		return api_dict

# function to display the data
@page_template('webapp/entry_index_page.html') 
def entry_index(
        request, template='webapp/entry_index.html', extra_context=None):
    context = {
        'images':  Image.objects.all()
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


# function to search for desired tags
def search(request):
	if 'q' in request.GET and request.GET['q']:
		TAG = request.GET['q']
	if 'start' in request.GET and request.GET['start']:
		START = parse_date(request.GET['start'])
		END = parse_date(request.GET['end'])
	store_data(TAG, START, END)
	return render(request, 'webapp/base.html')

# function to store posts in the database
def store_data(TAG, START, END):
	Image.objects.all().delete()
	img_counter = 1

	next_url = '%s/tags/%s/media/recent?client_id=%s&count=33' % (API_PREFIX, TAG, CLIENT_ID)

	print "test2"
	response = urllib2.urlopen(next_url)
	next_url1 = json.load(response)   

	date = int(next_url1['data'][0]['created_time'])
	pic_time = datetime.datetime.fromtimestamp(date)
	pic_date = pic_time.strftime('%Y-%m-%d')
	# pic_date1 = datetime.datetime.strptime(pic_date, '%Y-%m-%d')
	pic_date = parse_date(pic_date)
	print pic_date
	print "split"
	print START

	# Every time we load, we iterate 5 times
	while True:
		outdated = False 
		# request the data at that endpoint
		instagram_dict = make_api_request(next_url)
		try:
			next_url = instagram_dict['pagination']['next_url']
			instagram_data = instagram_dict['data']
			# for every picture tagged 
			for pic_dict in instagram_data:
				img_link = pic_dict['link']
				print 'start'
				print START
				print 'end'
				print END
				try:
					if TAG in pic_dict['caption']['text']:
					# get picture upload time and converts into YMD format
						pic_time_unix2 = int(pic_dict['caption']['created_time'])
						pic_time2 = datetime.datetime.fromtimestamp(pic_time_unix2)
						pic_date2= pic_time2.strftime('%Y-%m-%d')
						pic_date2 = parse_date(pic_date2)
						print 'caption'
						print pic_date2
						date_checking = pic_date2 + datetime.timedelta(days=3)
						if date_checking >= pic_date:
							pic_date = pic_date2
				except:
					print "no caption"

				for comment in pic_dict['comments']['data']:
					if TAG in comment['text']:
						print 'comment'
						pic_time_unix1 = int(comment['created_time'])
						pic_time1 = datetime.datetime.fromtimestamp(pic_time_unix1)
						pic_date1 = pic_time1.strftime('%Y-%m-%d')
						# pic_date1 = datetime.datetime.strptime(pic_date, '%Y-%m-%d')
						pic_date1 = parse_date(pic_date1)
						if pic_date1 >= pic_date:
							pic_date = pic_date1
		
				if pic_date > END:
					# DATE
					try: 
						pic_time_unix = int(pic_dict['caption']['created_time'])
						pic_time = datetime.datetime.fromtimestamp(pic_time_unix)
						pic_date = pic_time.strftime('%Y-%m-%d')
						pic_date = parse_date(pic_date)
						print 'caption'
						print "Desired end date is earlier than recent pic date"

					except:
						print "no caption"
					for comment in pic_dict['comments']['data']:
						if TAG in comment['text']:
							print 'comment'
							pic_time_unix1 = int(comment['created_time'])
							pic_time1 = datetime.datetime.fromtimestamp(pic_time_unix1)
							pic_date1 = pic_time1.strftime('%Y-%m-%d')
							pic_date1 = parse_date(pic_date1)
							if pic_date1 >= pic_date:
								pic_date = pic_date1
							
				elif (pic_date >= START) & (pic_date <= END):
					try:
						if TAG in pic_dict['caption']['text']:
						# get picture upload time and converts into YMD format
							pic_time_unix2 = int(pic_dict['caption']['created_time'])
							pic_time2 = datetime.datetime.fromtimestamp(pic_time_unix2)
							pic_date2= pic_time2.strftime('%Y-%m-%d')
							pic_date2 = parse_date(pic_date2)
							print 'caption'
							print pic_date2
							date_checking = pic_date2 + datetime.timedelta(days=3)
							if date_checking >= pic_date:
								pic_date = pic_date2
					except:
						print "no caption"

					for comment in pic_dict['comments']['data']:
						if TAG in comment['text']:
							print 'comment'
							pic_time_unix1 = int(comment['created_time'])
							pic_time1 = datetime.datetime.fromtimestamp(pic_time_unix1)
							pic_date1 = pic_time1.strftime('%Y-%m-%d')
							pic_date1 = parse_date(pic_date1)
							if pic_date1 >= pic_date:
								pic_date = pic_date1

					# download the photo and save it
					if pic_dict['type'] == 'image':
						image = pic_dict['images']['low_resolution']
						img_url = image['url']
						img_tag = TAG
						img_datatype = 'image'
					else:
						image = pic_dict['videos']['low_resolution']
						img_url = image['url']
						img_tag = TAG
						img_datatype = 'video'

					# save user id and username to get their info later
					username = pic_dict['user']['username']

					# putting into image database
					Image.objects.create(id=img_counter, Likes=pic_dict['likes']['count'], User=username,
						image_url=img_url, image_link = img_link, image_datatype = img_datatype, 
						post_date = pic_date)

					# retrieve the records from the database
					img_counter += 1
				else:
					outdated = True
					print img_link
					break
					
			if outdated:
				break
		except:
			print "No posts found."
			break



