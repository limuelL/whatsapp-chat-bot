# Whatsapp-Chat-Bot

This is a basic chatbot that uses Twilio and the Django Framework running on the Heroku platform.<br/>
<br/>
This bot is only composed of two commands.<br/>
- **gotrans** - to translate any languages to international language (English).<br/>
- **coinfo** - to get any cryptocurrency informations including the price, marketcap, volume, etc.<br/><br/>

This uses googletrans python module to translate languages and Coingecko api to access cryptocurrency prices.<br/>

## Quick Guide
1. Create a [twilio](https://www.twilio.com/) account and acquire a whatsapp number, SID and Auth Token.<br/>
2. Go to `message/views` and update your whatsapp number in the `send_message function".
3. Create a heroku app and add your SID, Auth token and Django SECRET KEY in configuration variables.<br>
4. Copy your heroku app url and go to your Twilio account, then replace the webhook url in the Whatsapp Sandox Settings.<br/><br/>

Horraaay! Your chatbot is now live.<br/>

## Todo
> Add more commands


