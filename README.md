# PiBitcoinPriceChecker
Display the bitcoin price on 7-segment led array close  to real-time.

## Appearance

## Components
- Raspberry Pi (We checked the operation of Pi 3 model B)
- 7-segment led array which can display 8 digits
- Wire (in order to connect raspberry pi with led)

## Motion of this program
- Run the DisplayController process and BitcoinPriceGetter process. 
- DisplayController control the GPIO of raspberry pi (using dynamic lighting system). 
- BitcoinPriceGetter get the bitcoin price(JPY) using the public API of coincheck(https://coincheck.com/api/rate/btc_jpy). 
- DisplayController get the bitcoin price from DisplayController process and display it.

## Usage
1. Connect Raspberry Pi with led in accordance with the following image.
2. Clone this repository on raspberry pi.
3. Exec following command on terminal.
`~`
