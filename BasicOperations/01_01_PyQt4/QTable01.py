filter_list为QTableWidget类型

#得到总行数
rows = self.filter_list.rowCount()

for rows_index in range(rows):
    #print items[item_index].text()
    print self.filter_list.item(rows_index,0).text()
    
    
tableWidget.currentRow()  ##可以获取一行的行号
QModelIndexList QTableView::selectedIndexes



// QTableWidget选中所有单元格及取消选中所有单元格

//    ui->allowSelectKeyTableWidget->selectAll();

//    ui->allowSelectKeyTableWidget->setFocus();

    introwCount=ui->TableWidget->rowCount();

    qDebug()<<"rowcount"<<rowCount;

    intcolCount=ui->TableWidget->columnCount();

    qDebug()<<"colcount"<<colCount;

    QTableWidgetSelectionRangerange(0,0,rowCount-1,colCount-1);

    ui->TableWidget->setRangeSelected(range,true);//false不选中

    ui->TableWidget->setFocus();


QList<QTableWidgetItem*>items=ui->TableWidget->selectedItems();

intcount=items.count();

for(inti=0;i<count;i++)

    {

       introw=ui->TableWidget->row(items.at(i));//获取选中的行

       QTableWidgetItem*item=items.at(i);

       QStringname=item->text();//获取内容

    }

 

方法二：获取选中的行

QList<QTableWidgetSelectionRange>ranges=ui->TableWidget->selectedRanges();

    intcount=ranges.count();

    for(inti=0;i<count;i++)

    {

       inttopRow=ranges.at(i).topRow();

       intbottomRow=ranges.at(i).bottomRow();

       for(intj=topRow;j<=bottomRow;j++)

       {

          qDebug()<<"selectRow"<<j;

        }

}
    
    
    以前使用QTableWidget时，窗口固定大小，可以设置最后一览固定大小，但是如果窗口自适应，那最后一览常常出现问题，还好Qt有自己的解决方法，代码:
[cpp] view plaincopyprint?在CODE上查看代码片派生到我的代码片

    QTableWidget *logTableWidget = new QTableWidget;  
    ui->logTableWidget->setColumnCount(3);  
    QStringList header;  
    header<<"time" << "tag" << "log";  
    ui->logTableWidget->setHorizontalHeaderLabels(header);  
    ui->logTableWidget->horizontalHeader()->setStretchLastSection(true);//关键  

    ui->logTableWidget->setColumnWidth(0, 100);  
    ui->logTableWidget->setColumnWidth(1, 100);  
    ui->logTableWidget->setContextMenuPolicy(Qt::CustomContextMenu);  
    ui->logTableWidget->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);      
