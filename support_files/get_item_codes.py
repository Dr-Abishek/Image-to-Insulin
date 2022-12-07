#Read the text file and obtain the item codes
def item_codes(txt_path):
  f = open(txt_path+".txt", "r")
  text_result = f.read()
  item_codes_from_text = []
  list_from_text = text_result.split()
  for i in range(len(list_from_text)):
      code = int(float(list_from_text[i]))
      if float(list_from_text[i]) == code:
          #if list_from_text[i] not in item_codes_from_text:
          item_codes_from_text.append(list_from_text[i])
  return(item_codes_from_text)
