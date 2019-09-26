# Steam Price Monitor
Python script to monitor price of objects on Steam Community Marketplace in realtime.

## Usage
Simply run the file.
* Default output currency: INR
* Default search app: CSGO
* Default search item: USP-S | Cortex (Minimal Wear)

------------

To change these values, make changes in **steam_monitor.py**

 - Change **CURRENCY** to desired currency.
 - Change **APP_ID** to desired game.
 - Change **POSITION** to desired item in **hash_names**.
 
![alt text](https://raw.githubusercontent.com/ByteBaker/steam_price_monitor/master/Images/EditCode.JPG)

Only items stored in **hash_names** can be searched.

To add another item in **hash_names**, find the complete item name as highlighted in the below picture by searching it on Steam. **USP-S | Cortex (Minimal Wear)** in this case. Add the name to **hash_names** in **steam_monitor.py**. Add as many names as you want. ADDING INCOMPLETE NAME MAY CAUSE THE TOOL TO BREAK.

![alt text](https://github.com/ByteBaker/steam_price_monitor/blob/master/Images/FindSearchString.JPG)


 To find an app ID, do a filtered search on Steam Community Market, and from the URL, take the value of **appid**
 
 For Example:
 
 In `https://steamcommunity.com/market/search?appid=730&q=usps+cortex+minimal+wear`
 
 `730 is the value of appid, which corresponds to CSGO`

## Have fun!

@ ByteBaker
