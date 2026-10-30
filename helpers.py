def youtube_id(url):
    url = url.strip()
    markers = ["watch?v=", "youtu.be/", "/shorts/"]

    found_marker = None
    for marker in markers:
        if marker in url:
            found_marker = marker
            break

    if found_marker is None:
        return None

    after_marker = url.split(found_marker)[1]
    video_id = after_marker[:11]

    if len(video_id) == 11:
        return video_id
    else:
        return None

print(youtube_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
print(youtube_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s"))
print(youtube_id("https://youtu.be/dQw4w9WgXcQ?si=abc123"))
print(youtube_id("https://www.youtube.com/shorts/dQw4w9WgXcQ"))
print(youtube_id("https://example.com/video"))
print(youtube_id(""))


#def youtube_id(url):
    #url = url.strip()

    #if "watch?v=" in url:
    #    part = url.split("watch?v=")[1]
    #elif "youtu.be/" in url:
      #  part = url.split("youtu.be/")[1]
    #elif "/shorts/" in url:
     #   part = url.split("/shorts/")[1]
    #else:
     #   return None

    #video_id = part[:11]

    #if len(video_id) == 11:
     #   return video_id
    #else:
     #   return None