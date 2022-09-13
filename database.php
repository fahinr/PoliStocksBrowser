<?php
        $hostName = "127.0.0.1";
        $userName = "root";
        $password = "amadeus001";
        $databaseName = "stockX";
        $conn = new mysqli($hostName, $userName, $password, $databaseName);
        // Check connection
        if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
        }
        $db= $conn;
        $tableName="poliexample";
        $columns= ['id', 'politician','issuer','ticker','trade_date', 'type','size','price', 'analyst_rating'];
        $fetchData = fetch_data($db, $tableName, $columns);
        function fetch_data($db, $tableName, $columns){
            if(empty($db)){

                $msg= "Database connection error";
            }
            elseif (empty($columns) || !is_array($columns)) {
                $msg="columns Name must be defined in an indexed array";
            }
            elseif(empty($tableName)){
                $msg= "Table Name is empty";
            }
            else{
                $columnName = implode(", ", $columns);
                $query = "SELECT ".$columnName." FROM $tableName"." ORDER BY id DESC";
                $result = $db->query($query);
                if($result== true){ 
                    if ($result->num_rows > 0) {
                        $row= mysqli_fetch_all($result, MYSQLI_ASSOC);
                        $msg= $row;
                    } 
                    else {
                        $msg= "No Data Found"; 
                    }
                }
                else{
                    $msg= mysqli_error($db);
                }
            }

            return $msg;

            }
        ?>