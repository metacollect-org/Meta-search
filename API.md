#Meta-Search Api Documentation

This document shall provide all the necessary information about how to use the
Meta-Search API.

##Reaching the API

The API can be reached under <djangourl>/api/.

You can either perform full-text-search utilizing elastic-search, perform simple
database-queries using djangos Querysets or search for projects in a certain area.

The Different functions can be used under the following urls:




##Model

The Returned values will focus around our database objects, so, to kick things off, a short description of
our Objects and their JSON, XML and YAML representation.

###Category
Categories are used to tag the projects. Each category can have a parent, so
a hierarchical category structure is possible.

####JSON
```JSON
[{
	"id": 2412,
	"name": "german",
	"parent": 2315
}]
```
####XML

####YAML


###Kind

###Language

###Project

Project


##The `/api/search`-pages

Apart from the special pages mentioned above, you may also use the search api
for direct access to simple database queries.

You are able to filter specific elements based on certain fields. The general
syntax looks like this:
```
/api/search/<object_name>?<field_1>*<action1>=<val1>&<field_2>*<action2>=<val2>
```
Below follows a description of each parameter:
PARAMETER|DESCRIPTION
---------|------------
`<object_name>`|The name of the database objects, you are interested in, can be `project`, `category`, `kind` or `language`.
`<field>`|The name of a Database Field, you want to search on. at the end of this document, you get a list of all Fields for each
`<action>`| **Optional** The Field Lookups for django to use.
`<val>`| the Value, the specified field should have.


##Return Values

For all Requests, you can specify the return type by appending `format=XXX` to
the url. supported formats are JSON, YAML and XML.

```JSON
[{
	"id": 1034,
	"kind": [{
		"id": 13,
		"name": "website"
	}],
	"categories": [{
		"id": 2321,
		"name": "social life",
		"parent": null
	}, {
		"id": 2328,
		"name": "events",
		"parent": null
	}, {
		"id": 2335,
		"name": "coordination",
		"parent": null
	}, {
		"id": 2378,
		"name": "leisure",
		"parent": null
	}, {
		"id": 2385,
		"name": "social media",
		"parent": null
	}, {
		"id": 2402,
		"name": "facebook",
		"parent": null
	}],
	"languages": [{
		"id": 99,
		"name": "german",
		"abbreviation": "de",
		"alternatives": "deutsch"
	}],
	"programming_languages": [],
	"title": "Welcome Challenge",
	"url": "http://www.welcomechallenge.de/",
	"organisation_name": "#Welcome Challenge",
	"description_de": "Challenge:1. Freunde aktivieren, die auch helfen wollen2. Plane und dokumentiere deine Hilfaktion3. Poste deine Hilfsaktion und aktiviere Freunde4. Die aktivierten Freunde beginnen wieder bei 1.",
	"description_en": "",
	"description_fr": "",
	"description_ar": "",
	"area_country": "Germany",
	"area_state": "Mecklenburg-Vorpommern",
	"area_city": "Rostock",
	"status": 1,
	"logo": "http://www.welcomechallenge.de/img/welcomechallenge-960.jpg",
	"contact_socialmedia_fb": "https://www.facebook.com/groups/welcomechallenge/?fref=ts",
	"contact_socialmedia_twitter": "",
	"contact_telephone": "",
	"contact_address_street": "Osloer Str. ",
	"contact_address_housenr": "28",
	"contact_address_zip": "18107",
	"contact_address_city": "Rostock",
	"contact_address_country": "Germany",
	"needs": "",
	"created_at": "2016-01-18T14:40:04.763514Z",
	"updated_at": "2016-02-01T09:58:19.694490Z",
	"geo_location": 218,
	"contact_loc": null
}]
```

###Sample requests

`api/search/project?title*icontains=refugee`










