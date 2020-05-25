import pandas as pd

from io import StringIO, BytesIO


class CSVRender(object):

   @staticmethod
   def render(content):
       output = StringIO()
       df = pd.DataFrame(data=content)
       df.to_csv(output, index=False, sep=';')
       output.seek(0)
       # NOTE: This was made this way because Flask ONLY can send bytes
       # but pandas needs a StrinIO to get everything works.
       buf = BytesIO()
       buf.write(output.read().encode())
       buf.seek(0)
       return buf
