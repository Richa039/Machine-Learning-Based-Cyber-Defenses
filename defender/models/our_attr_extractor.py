import lief
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import scipy
import re
import time
class CustomPEExtractor():


    # initialize extractor
    def __init__(self, binary_file, vect):
        self.binary = lief.PE.parse(list(binary_file))
        self.tokenizer = vect
    # def preprocess(self, entry):
    #   entry = entry.replace(':', '').replace('-', ' ')
    #   entry = entry.replace('\n', ' ')
    #   entry = ' '.join(entry.split())
    #   return entry
    def time_it(func):
      def wrapper(*args, **kwargs):
          start_time = time.time()
          result = func(*args, **kwargs)
          end_time = time.time()
          print(f"Function '{func.__name__}' took {end_time - start_time} seconds to execute")
          return result
      return wrapper
    
    @time_it
    def preproc(self, entry):
      pattern = r'\b\w+:\b'
      entry = re.sub(pattern, '', entry)
      entry = entry.replace(':', '').replace('-', ' ')
      entry = entry.replace('\n', ' ')
      entry = ' '.join(entry.split())
      return entry
    
    @time_it
    def parse_exe(self, exe_path):
        # parse the executable using lief
        # print("Trimmed text is: ", trimmed)
        # pe_string = preprocess(str(pe).replace(str(pe.get_import), ""))
        entry = str(self.binary).replace(str(self.binary.get_import), "")
        # print(type(pestr))
        # pattern = r'\b\w+:\b'
        # cleaned_text = re.sub(pattern, '', entry)
        # entry = entry.replace(':', '').replace('-', ' ')
        # entry = entry.replace('\n', ' ')
        # entry = ' '.join(entry.split())
        trimmed = self.preproc(entry)
        return trimmed

      
    @time_it
    def tokenization(self, input_string):
      
    #   print("Input string is: ", input_string)
      tokenized_texts = self.tokenizer.transform([input_string])

    #   print(padded_sequences)

      return tokenized_texts
    
    # extract attributes
    @time_it
    def extract(self):
      
      input_df = self.parse_exe(self.binary)

      output_tokens = self.tokenization(input_df)

      # print(output_tokens)

      return output_tokens
      
      
      
      