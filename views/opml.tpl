<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
 <head>
   <title>RSS feeds</title>
 </head>
 <body>

  % for name_item,url_item in zip(name,url):
     <outline text="{{name_item}}" description="{{name_item}}" xmlUrl="{{url_item}}" type="rss" />
  % end

 </body>
</opml>