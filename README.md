# booksusi

# add ssh

ssh-keygen -t rsa -b 4096 -C “your_comment_or_email”

eval $(ssh-agent -s)

ssh-add ~/.ssh/id_rsa

# Copy the public key to the clipboard with command and add to guthub
clip < ~/.ssh/id_rsa.pub
# Test connection with command 
ssh -T git@github.com

#check which branches are available
git branch -v -a

# git add
git init

git remote add origin git@github.com:flabbrgastr/booksusi.git

git fetch
