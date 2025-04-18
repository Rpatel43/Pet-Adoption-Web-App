"# cse2102-spring25-Team29
Ronit Patel rop21003" 
Joseph Pizzuti jop19011
Saoudkhan pathan Sap21027
Rayna Spicher rcs20010
https://trello.com/b/0zbMYZli/cse2102-team29
https://www.figma.com/design/0H0O1hAC6xJz2soKSml86l/CSE2102-Site-Prototype?node-id=0-1&t=XUrpxJiLNF33jHGe-1

# getting repo locally and getting db
1. clone repo
2. pip install -r requirements.txt
3. generate key: 'export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32)")
4. flask init-database
5. flask run --host=0.0.0.0

# docker
1. 'docker build -t team29/pet-adopt-api:latest .
2. 'docker run --rm -p 5000:5000 \ -e SECRET_KEY=${SECRET_KEY} \ team29/pet-adopt-api:latest
