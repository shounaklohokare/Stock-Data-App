from tkinter import *  # Importing tkinter package
from yahoo_fin.stock_info import *  # Importing yahoo_fin package which is used to get stock data

root = Tk()  # Declaring main window of Tkinter

root.geometry("600x290")  # declaring size of window

color = "honeydew2"

root.title("Stock Data App")
p1 = PhotoImage(file="img_462278.png")
root.iconphoto(False, p1)

frame = LabelFrame(root, text="Stock Data App", bg=color)
frame.pack(fill="both", expand="yes")

lbl = Label(frame, text="Enter the Stock Ticker Symbol:", font=("Bold Courier", 11), bg=color)
lbl.grid(column=0, row=0, padx=(60, 5), pady=(23, 4))

tickerVar = StringVar()


def caps(event):
    """
    Converts all letters enterted into Entry widget capital.
    """
    tickerVar.set(tickerVar.get().upper())


e = Entry(frame, textvariable=tickerVar, bd=6)  # Declaring and setting the entry widget
e.grid(column=1, row=0, padx=(0, 10), pady=(23, 4))
e.bind("<KeyRelease>", caps)

exchanges = ["    NSE    ", "NASDAQ"]

ExchangeVar = StringVar()
ExchangeVar.set(exchanges[0])

ExchangeOptions = OptionMenu(frame, ExchangeVar, *exchanges)
ExchangeOptions.grid(row=0, column=2, padx=(0, 50), pady=(22, 4))

nframe = LabelFrame(frame, bg="papayawhip", bd=5)
nframe.grid(row=2, column=0, padx=26, pady=10, columnspan=5)


def getPrice():
    """
    Extracts the stock ticker symbol from Entry widget data and after extracting the information through yahoo_fin package
    displays it on the Label widget.
    """
    root.geometry("600x460")  # resizes the root window to accommodate the stock data which is to be displayed
    try:

        for widget in nframe.winfo_children():
            widget.destroy()

        ticker = tickerVar.get()  # gets the stock ticker symbol from Entry widget

        if ticker.strip() == "":
            lbl = Label(nframe, text="You cannot leave the entry widget blank, please enter a stock ticker symbol.",
                        font=("Bold Courier", 11), relief="flat", bg=color)
            lbl.pack()
            e.delete(0, END)

        else:
            if ExchangeVar.get().strip() == 'NSE':  # If Option Menu has NSE exchange selected appends .NS to ticker
                ticker += '.NS'
                quotesTableDict = get_quote_table(ticker)  # gets the stock data from function of yahoo_fin package
                openP, prevClose, _1YearTargetEstimate = quotesTableDict['Open'], quotesTableDict['Previous Close'], \
                                                         quotesTableDict['1y Target Est']
                price = "₹" + str(round(float(get_live_price(ticker)),
                                        2))  # adds rupee symbol as a suffix to attributes of NSE stocks
                openP = "₹" + str(openP)
                prevClose = "₹" + str(prevClose)
                _1YearTargetEstimate = "₹" + str(_1YearTargetEstimate)


            else:
                quotesTableDict = get_quote_table(ticker)  # gets the stock data from function of yahoo_fin package
                openP, prevClose, _1YearTargetEstimate = quotesTableDict['Open'], quotesTableDict['Previous Close'], \
                                                         quotesTableDict['1y Target Est']
                price = "$" + str(round(float(get_live_price(ticker)),
                                        2))  # adds dollar symbol as a suffix to attributes of NASDAQ stocks
                openP = "$" + str(openP)
                prevClose = "$" + str(prevClose)
                _1YearTargetEstimate = "$" + str(_1YearTargetEstimate)

            _52WeekRange = quotesTableDict['52 Week Range']
            lastDividend, marketCap = quotesTableDict['Ex-Dividend Date'], quotesTableDict['Market Cap']
            volume = quotesTableDict['Volume']

            nframe.configure(text=tickerVar.get())

            if str(lastDividend) == "nan":
                lastDividend = "No Dividend Issued till date."

            if str(_1YearTargetEstimate) == '₹nan' or str(_1YearTargetEstimate) == '$nan':
                _1YearTargetEstimate = "Estimate is unavailable."

            display = f"""  \nTrading At: {ExchangeVar.get().strip()}
                            \nCurrent Price: {price}
                            \nOpen At: {openP}
                            \nPrevious Close: {prevClose}
                            \nLast Dividend: {lastDividend}
                            \n1 Year Target Estimate: {_1YearTargetEstimate}
                            \n52 week range : {_52WeekRange}
                            \nMarket Cap: {marketCap}
                            \nVolume: {volume}"""
            # sets all the atttributes of stocks to be displayed in the display variable

            lbl = Label(nframe, text=display, font=("Bold Courier", 11), relief="flat", bg="papayawhip",
                        justify="left")  # displays the dsiplay variable
            lbl.grid(row=0, column=0, padx=0)

            e.delete(0, END)

    except AssertionError:  # multiple exceptions to be handled
        nframe.configure(text="")
        lbl = Label(nframe,
                    text=f"You entered an invalid stock ticker '{tickerVar.get()}' doesn't exist at {ExchangeVar.get().strip()}",
                    font=("Bold Courier", 11), relief="flat", bg="papayawhip")
        lbl.pack()

        e.delete(0, END)


    except Exception as errr:
        nframe.configure(text="")
        if errr == "adjclose":
            lbl = Label(nframe,
                        text=f"You entered an invalid stock ticker '{tickerVar.get()}' doesn't exist at {ExchangeVar.get().strip()}",
                        font=("Bold Courier", 11), relief="flat", bg="papayawhip")
            lbl.pack()
            e.delete(0, END)

        else:
            lbl = Label(nframe,
                        text="An unexpected error has occurred, either you have entered an\ninvalid stock ticker symbol or your internet connection has failed.",
                        font=("Bold Courier", 11), relief="flat", bg="papayawhip")
            lbl.pack()
            e.delete(0, END)


b = Button(frame, text="Search", command=getPrice)  # button for search associated with the function getPrice()
b.grid(column=1, row=1, sticky=W, padx=(38, 0))

root.mainloop()
