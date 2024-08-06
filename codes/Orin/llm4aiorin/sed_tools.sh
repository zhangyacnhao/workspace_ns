

sed -i 's/config\[\([^]]*\)\]\[\([^]]*\)\]/os.path.expandvars(&)/g' *.py
sed -i '1i from dotenv import load_dotenv' *.py
sed -i '2i import os'  *.py
