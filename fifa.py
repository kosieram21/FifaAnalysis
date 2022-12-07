import warnings
import argparse
import preprocessCSVs
import initializeDB
import deleteDB
import printDB
import queryDB
import train_model


warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(prog="fifa",
                                 description="runs machine learning regression models on fifa women's world cup data")
parser.add_argument("-r", "--preprocess", help="preprocesses the csvs that contain the dataset", action="store_true")
parser.add_argument("-i", "--initialize", help="initialize the fifa database", action="store_true")
parser.add_argument("-d", "--delete", help="delete the fifa database", action="store_true")
parser.add_argument("-p", "--print", help="print the tables in the fifa database", action="store_true")
parser.add_argument("-q", "--query", help="queries the fifa database for interesting information", action="store_true")
parser.add_argument("-l", "--learn", help="trains a regression model on the fifa database", action="store_true")

args = parser.parse_args()

if args.preprocess:
    preprocessCSVs.execute()

DB = "fifa"
if args.initialize:
    initializeDB.execute(DB)
if args.delete:
    deleteDB.execute(DB)
if args.print:
    printDB.execute(DB)
if args.query:
    queryDB.execute(DB)
if args.learn:
    train_model.execute(DB)
