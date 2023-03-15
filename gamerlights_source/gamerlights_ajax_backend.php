<?php

header("Content-Type: application/json");

$requestInputString_json = file_get_contents('php://input');
$requestInputObject_json = json_decode($requestInputString_json, true);

if($requestInputObject_json['requestType'] == 'fetch'){
    $colorsStoredString_json = file_get_contents("colors.json");
    $colorsStoredObject_json = json_decode($colorsStoredString_json,true);
    
    echo json_encode(array(
        "success" => true,
        "time" => date("h:i:sa"),
        "staticColor" => array_values($colorsStoredObject_json["data"])[0]['staticColor'],
        "fadeColor1" => array_values($colorsStoredObject_json["data"])[0]['fadeColor1'], 
        "fadeColor2" => array_values($colorsStoredObject_json["data"])[0]['fadeColor2'], 
        "mode" => array_values($colorsStoredObject_json["data"])[0]['mode']
    ));
    exit;
}
elseif($requestInputObject_json['requestType'] == 'submit'){
    $JSONFilePreSubmit_string = file_get_contents("colors.json");
    $JSONFilePreSubmit_json = json_decode($JSONFilePreSubmit_string,true);
    unset($requestInputObject_json['requestType']);
    
    array_push($JSONFilePreSubmit_json["data"],$requestInputObject_json);
    $JSONFilePostSubmit_string = json_encode($JSONFilePreSubmit_json);
    file_put_contents("colors.json", $JSONFilePostSubmit_string);
    echo json_encode(array(
        "success" => true,
        "time" => date("h:i:sa"),
        "staticColor" => $requestInputObject_json['staticColor'],
        "fadeColor1" => $requestInputObject_json['fadeColor1'], 
        "fadeColor2" => $requestInputObject_json['fadeColor2'], 
        "mode" => $requestInputObject_json['mode']
    ));
    exit;
}
else{
    echo json_encode(array(
        "success" => false,
        "time" => date("h:i:sa")
    ));
    exit;
}

?>