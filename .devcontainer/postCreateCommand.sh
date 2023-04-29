#! /bin/bash

set -e
set -x

curl -f -o ~/.git-completion.bash \
    https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash

cat << EOF >> ~/.bashrc
if [ -f ~/.git-completion.bash ]; then
  . ~/.git-completion.bash
fi
EOF

pip completion --bash > ~/.pip-completion.bash
cat << EOF >> ~/.bashrc
if [ -f ~/.pip-completion.bash ]; then
  . ~/.pip-completion.bash
fi
EOF

make init