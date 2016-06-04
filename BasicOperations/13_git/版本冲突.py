两个用户a,b
pull完同一个github.ocm代码库在同时对同一个代码文件进行修改
修改后，a先做了push
之后b做push时，提示版本冲突
此时，b需要先pull，再add，再commit，再push
b再pull时，会提示需要做merge

这时的merge有两种方案：
1.丢弃本地修改，直接接受github.com文件
    git reset --hard
    git pull
2.选择将a,b的修改同时包含到冲突文件，由b手动修改
    git pull 后会提示如何操作
    
    
在两台电脑上使用同一个用户对代码库做改动时，最好的方式是：
    1.每次修改前
    pull
    2.每次修改完之后
    add，commit，push
    
    如此方能避免这个难搞的，也容易出错的文件冲突问题
