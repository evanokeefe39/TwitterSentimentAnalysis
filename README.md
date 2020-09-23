Create index
```
Invoke-RestMethod -Method PUT -Uri 'http://localhost:9200/sentiment'

```

Set the type mappings for the index
```
$body=@{properties= @{author= @{type="text"};date= @{type="date"};message= @{type= "text"}; polarity= @{type="float"}; subjectivity= @{type= "float"}; sentiment= @{type= "text"};};};

$json= $body |ConvertTo-Json

$mapping = $endpoint + '/_mapping'

$contentType3 = "application/json" 

Invoke-RestMethod -Method PUT -Uri $mapping -ContentType $contentType3 -Body $json;

```

Clear all indices
```
Invoke-WebRequest -method DELETE $url + '_all'

```
