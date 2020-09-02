from pandas_datareader import data as pdr
import yfinance as yf
import datetime



yf.pdr_override()
class YFinance():
    @staticmethod
    def Fetch1Year(Symbol):
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.date.today()- datetime.timedelta(days=1)
        yahoo_df = pdr.get_data_yahoo(Symbol, start=start_date, end=end_date)

        return yahoo_df


