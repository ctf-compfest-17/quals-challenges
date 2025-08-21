# Writeup Mr & Mrs Smith

According to the description, start by looking at the most time usage of the phone.

1. Application usage statistics:
 ..\data\data\com.google.android.apps.turbo\shared_prefs\app_usage_stats.xml 
 The highest will be com.google.android.apps.messaging
2. Chat messaging:
..\data\data\com.google.android.apps.messaging\databases\bugle_db
 saying "We upload our work here: https://drive.google.com/drive/folders/1wfF_RRAp_dyzDzHeNJhe4CvZNs9qbwUK?usp=sharing" "It's encrypted with the date of our first date-location, like 23122025-londonbridge"
3. Calendar:
..\data\data\com.android.providers.calendar\databases\calendar.db 
Calendar to get the anniv date (events table, number 16), there is a note stating: "We started dating, and took a picture to commemorate it" 
4. Images: 
..\data\media\0\DCIM\Camera\IMG_2119.jpg
Shows a couple image with the date, and location metadata
5. Drive link:
https://drive.google.com/drive/folders/1wfF_RRAp_dyzDzHeNJhe4CvZNs9qbwUK?usp=sharing
Download classified.pdf.gpg, unlock with the password 03032020-centralpark. The flag will be found inside.