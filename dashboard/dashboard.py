import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
import os

all_df = pd.read_csv("combined_dataset.csv")

all_df.info()
all_df.head()
