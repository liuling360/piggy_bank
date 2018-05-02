    redis-cli -h @endpoint -a @user keys "$Today*" | xargs redis-cli -h @endpoint -a @user del
