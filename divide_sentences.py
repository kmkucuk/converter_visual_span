import pandas as pd

def split_into_lines(text, length=20):
    text = str(text)  # ensure it's a string
    line1 = text[0:length]
    line2 = text[length:length*2]
    line3 = text[length*2:length*3]
    return pd.Series([line1, line2, line3])

def main():
    # Load CSV file
    df = pd.read_excel("mnread_all_list.xlsx")  
    df[['line1', 'line2', 'line3']] = df['sentence'].apply(split_into_lines)
    df.to_excel("output_with_lines.xlsx", index=False)

if __name__ == "__main__":    
    main()
    print(f'Sentences divided into three lines')
