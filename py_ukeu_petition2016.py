# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 10:53:55 2016

@author: memo

plot petition signatures by country, specifically, petition for 2nd referendum on UK EU vote
"EU Referendum Rules triggering a 2nd EU Referendum"
https://petition.parliament.uk/petitions/131215

"""

import json
import urllib
import numpy as np
import matplotlib.pyplot as plt



# load from local file or from online url
do_load_local = False

# path to local data
data_path = '131215.json'

# url to online data
data_url = 'https://petition.parliament.uk/petitions/131215.json'

# only include top xxxx countries in graph
#top_country_count = 150
top_country_count = -1

# class to load Peition from local data file or online url
class Petition:
    def __init__(self, url, local):
        # load data (from local file or online url)
        if local:
            print 'loading from file', url
            self.json_data = json.loads(open(url).read())
        else:
            print 'loading from url', url
            response = urllib.urlopen(url)
            self.json_data = json.loads(response.read())
        
        # get metadata    
        self.data = self.json_data['data']
        self.dattr= self.data['attributes']
        
        self.title              = self.dattr['action']
        self.creator            = self.dattr['creator_name']
        self.total_sig_count    = self.dattr['signature_count']
        self.update_date        = self.dattr['updated_at']

        # get signatures by country
        self.sigs_by_country = self.dattr['signatures_by_country']
        self.num_countries = len(self.sigs_by_country)

        print self.title
        print 'by', self.creator
        print self.total_sig_count, 'signatures at', self.update_date
        print 'in', self.num_countries, 'countries'
        
        

# load data (from local file or online url)
if do_load_local:
    p = Petition(data_path, local=True)
else:
    p = Petition(data_url, local=False)
    print 'loading from url', data_url
   


# sort countries by signature count
sigs_by_country = sorted(p.sigs_by_country, key=lambda k: k['signature_count'], reverse=True) 


# number of signatures outside 
sig_count_outside_top = p.total_sig_count - sigs_by_country[0]['signature_count']
s_sigs_outside = '(' + str(sig_count_outside_top) + ' signatures outside ' + sigs_by_country[0]['name'] + ')'
print s_sigs_outside

# only include top xxxx countries in graph
if top_country_count < 0:
    top_country_count = p.num_countries
    
sigs_by_country = sigs_by_country[:top_country_count]

# separate names and counts
country_names = [ x['name'] for x in sigs_by_country ]
country_sig_count = np.array([ x['signature_count'] for x in sigs_by_country ])

# get sig count not in top xxxx countries
sig_count_remain = p.total_sig_count - np.sum(country_sig_count)


country_names.append('OTHER')
country_sig_count = np.append(country_sig_count, sig_count_remain)


labels = country_names
y = country_sig_count
x = np.arange(len(y))

fig,ax = plt.subplots()
fig.set_size_inches(40, 10)
plt_title = 'top ' + str(top_country_count) + ' (out of ' + str(p.num_countries) + ') countries who signed: '
plt_title += "'" + p.title + "' on " + p.update_date + '\n'
plt_title += 'data at: https://petition.parliament.uk/petitions/131215\n'
plt_title += 'py src for plt at: https://github.com/memo/py_ukeu_petition2016\n'
plt_title += 'NOTE: LOG SCALE FOR READABILITY (i.e. bar heights not linearly proportional)'
ax.set_title(plt_title)
ax.set_ylabel('# signatures (log)')
ax.set_xticks(x + 0.4)
ax.set_xticklabels(labels, rotation = 90)
bars = plt.bar(x, y, log=True)
for r in bars:
    h = r.get_height()
    ax.text(r.get_x() + r.get_width()/2., h * 1.1, 
            '%d' % int(h),
            ha='center', va='bottom', rotation=90)


plt.show()
plt.savefig('fig.png', dpi=150, bbox_inches='tight')