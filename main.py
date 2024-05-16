import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom


def main(input_file_name, url_column_index, output_file_name, last_modified_date_string=None):
  urlset = ET.Element("urlset")
  urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
  urlElement = ET.SubElement(urlset, "script")
  
  destinationUrlList = []
  uniqueUrlCount = 0

  with open(input_file_name, "r", newline='', encoding='utf-8') as redirectTable:
    reader = csv.reader(redirectTable)
    headers = next(reader)

    # リダイレクト表の遷移先 URL からリストを作成
    for row in reader:
      destinationUrlList.append(row[url_column_index])
      
  # 重複する URL を排除して <url> 要素を作成
  for item in sorted(set(destinationUrlList), key=len):
    urlElement = ET.SubElement(urlset, "url")
    locElement = ET.SubElement(urlElement, "loc")
    locElement.text = item
    if last_modified_date_string != None:
      lastmodElement = ET.SubElement(urlElement, "lastmod") 
      lastmodElement.text = last_modified_date_string
    uniqueUrlCount += 1

  # XML にパースしてファイル出力
  xml_string = minidom.parseString(ET.tostring(urlset, 'utf-8'))
  try: 
    with open(output_file_name, "w", encoding='utf-8') as siteMap:
      xml_string.writexml(siteMap, encoding='utf-8', newl='\n', indent='', addindent='  ')
      print(f"{output_file_name}に{uniqueUrlCount}個のURLを書き込みました。")
  except Exception as e:
    print(f"ファイル書き込みでエラーが発生しました。{e}")


main('redirectTable.csv', 3, 'sitemap.xml')
# main('redirectTable.csv', 3, 'sitemap.xml', '2024-05-29')
