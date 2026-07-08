from paddleocr import PaddleOCR

class OCRService:

    def __init__(self):
      self.ocr=PaddleOCR(use_angle_cls=True,lang='en')


    def extract_text(self,image_path):
         
        result=self.ocr.ocr(image_path)

        texts=[]

        for page in result:
           if page is None:
              continue
           
           for line in page:
              
              texts.append({
                 "text":line[1][0],
                 "confidence":float(line[1][1])
              })
        return {
        "status": "PASS",
        "total_lines": len(texts),
        "results": texts
    }
      
