<?php
require_once('../vendor/autoload.php');
$host = [
    '39.108.78.17:9200'
];
$es = Elasticsearch\ClientBuilder::create()->setHosts($host)->build();

$query = $_POST['query'];
$query = strtolower($query);

$head =<<<HEAD
<!DOCTYPE html>
<html>
<head lang="en">
  <meta charset="UTF-8">
  <title>XDsearch</title>
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="format-detection" content="telephone=no">
  <meta name="renderer" content="webkit">
  <meta http-equiv="Cache-Control" content="no-siteapp" />
  <link rel="alternate icon" type="image/png" href="../assets/i/favicon.png">
  <link rel="stylesheet" href="../assets/css/amazeui.min.css"/>
  <style>
    .header {
      text-align: center;
    }
    .header h1 {
      font-size: 200%;
      color: #333;
      margin-top: 30px;
    }
    .header p {
      font-size: 14px;
    }
  </style>
</head>
<body>
<div class="header">
  <div class="am-g">
    <h1 style='font-size:81px;font-weight:bold;'>XDsearch</h1>
  </div>
</div>
<div class="am-g">
  <div class="am-u-lg-6 am-u-md-8 am-u-sm-centered">
    <form  action='./queryHandler.php' method="post" class="am-form">
      <input type="text" name="query" id="email" value="$query">
<input type="submit" hidden='hidden'  value="Submit" />
    </form>
  </div>
</div>
<br />
HEAD;

echo $head;
//请求
$json = array(
    "body" => [
    "query" => [
        "bool" => [
            "should" => [
                ["match" => ["url" => $query]],
                ["match" => ["url.en" => $query]],
                ["wildcard" => ["url.cn" => "*".$query."*"]],
                ["wildcard" => ["title.cn" => "*".$query."*"]],
                ["match" => ["title.cn" => ["query" => $query, "boost" => 50]]],
                ["match" => ["body.cn" => $query]],
                ["match" => ["body.py" => $query]],
                ["match" => ["title.py" => $query]],
            ],
            "minimum_should_match" => 1,
        ],
    ],
    "highlight" => [
        "pre_tags" => ["<font color='red'>"],
        "post_tags" => ["</font>"],
        "fields" => [
            "url" => (object) array(),
            "url.en" => (object) array(),
            "url.cn" => (object) array(),
            "title" => (object) array(),
            "title.en" => (object) array(),
            "title.cn" => (object) array(),
            "title.py" => (object) array(),
            "body.py" => (object) array(),
            "body" => (object) array(),
            "body.en" => (object) array(),
            "body.cn" => (object) array(),
        ],
    ],
],
);

$json1 = array(
    "body" => [
    "query" => [
        "bool" => [
            "should" => [
                ["match" => ["url" => $query]],
                ["match" => ["url.en" => $query]],
                ["wildcard" => ["url.cn" => "*".$query."*"]],
                ["match" => ["title.cn" => ["query" => $query, "boost" => 50]]],
                ["match" => ["body.cn" => $query]],
            ],
            "minimum_should_match" => 1,
        ],
    ],
],
);

$re = $es->search($json);
$count = $re["_shards"]["total"];
$hits = $re["hits"];
$hits = $hits["hits"];
foreach ($hits as $v) {
    $source = $v["_source"];
    $highlight = $v["highlight"];
    $url = $source["url"];
    $title = isset($highlight["title.cn"][0]) ? $highlight["title.cn"][0] : (isset($highlight["title.py"][0]) ? $highlight["title.py"][0] : $source["title"]);
    $body = isset($highlight["body.cn"][0]) ? $highlight["body.cn"][0] : (isset($highlight["body.py"][0]) ? $highlight["body.py"][0] : $source["body"]);
    $hit = <<<INDEX
<div align="left"><a target="_blank" style="margin-left:7%;" href="http://$url">$title</a></div>
<div style="word-wrap:break-word; word-break:break-all; overflow: hidden; height:50px; width:70%; margin-left:7%;">
<p>$body</p>
</div>
<div style="word-wrap:break-word; word-break:break-all; overflow: hidden; height:60px; width:70%; margin-left:7%;">
<font size="2" stlye="margin-left:7%;" color="green">http://$url</font>
</div>
<br/>
INDEX;
    echo $hit;
}
$end = <<<END
<script type="text/javascript" opacity="1" count="150" zIndex="-2"  color="0,134,139"  src="./canvas.js"></script></body></html>
END;

echo $end;
?>
