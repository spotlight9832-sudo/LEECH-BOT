from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig
from time import sleep
from qbittorrentapi import NotFound404Error, Client as qbClient
from aria2p import API as ariaAPI, Client as ariaClient
from flask import Flask, request

from web.nodes import make_tree

app = Flask(__name__)

aria2 = ariaAPI(ariaClient(host="http://localhost", port=6800, secret=""))

basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s",
            datefmt="%d-%b-%y %I:%M:%S %p",
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)

LOGGER = getLogger(__name__)

page = """
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Torrent File Selector</title>
    <link rel="icon" href="https://graph.org/file/1a6ad157f55bc42b548df.png" type="image/jpg">
    <script
      src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
      integrity="sha256-4+XzXVhsDmqanXGHaHvgh1gMQKX40OUvDEBTu8JcmNs="
      crossorigin="anonymous"
    ></script>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css"
      integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p"
      crossorigin="anonymous"
    />
<style>

*{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Ubuntu", sans-serif;
    list-style: none;
    text-decoration: none;
    outline: none !important;
    color: white;
}

body{
    background-color: #0D1117;
}

header{
    margin: 3vh 1vw;
    padding: 0.5rem 1rem 0.5rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: #161B22;
    border-radius: 30px;
    background-color: #161B22;
    border: 2px solid rgba(255, 255, 255, 0.11);
}

header:hover, section:hover{
    box-shadow: 0px 0px 15px black;
}

.brand{
    display: flex;
    align-items: center;
}

img{
    width: 2.5rem;
    height: 2.5rem;
    border: 2px solid black;
    border-radius: 50%;
}

.name{
    margin-left: 1vw;
    font-size: 1.5rem;
}

.intro{
    text-align: center;
    margin-bottom: 2vh;
    margin-top: 1vh;
}

.social a{
    font-size: 1.5rem;
    padding-left: 1vw;
}

.social a:hover, .brand:hover{
    filter: invert(0.3);
}

section{
    margin: 0vh 1vw;
    margin-bottom: 10vh;
    padding: 1vh 3vw;
    display: flex;
    flex-direction: column;
    border: 2px solid rgba(255, 255, 255, 0.11);
    border-radius: 20px;
    background-color: #161B22 ;
}

li:nth-child(1){
    padding: 1rem 1rem 0.5rem 1rem;
}

li:nth-child(n+1){
    padding-left: 1rem;
}

li label{
    padding-left: 0.5rem;
}

li{
    padding-bottom: 0.5rem;
}

span{
    margin-right: 0.5rem;
    cursor: pointer;
    user-select: none;
    transition: transform 200ms ease-out;
}

span.active{
    transform: rotate(90deg);
    -ms-transform: rotate(90deg); /* for IE  */
    -webkit-transform: rotate(90deg);/* for browsers supporting webkit (such as chrome, firefox, safari etc.). */
    display: inline-block;
}

ul{
    margin: 1vh 1vw 1vh 1vw;
    padding: 0 0 0.5rem 0;
    border: 2px solid black;
    border-radius: 20px;
    background-color: #1c2129;
    overflow: hidden;
}

input[type="checkbox"]{
    cursor: pointer;
    user-select: none;
}

input[type="submit"] {
    border-radius: 20px;
    margin: 2vh auto 1vh auto;
    width: 50%;
    display: block;
    height: 5.5vh;
    border: 2px solid rgba(255, 255, 255, 0.11);
    background-color: #0D1117;
    font-size: 16px;
    font-weight: 500;
}

input[type="submit"]:hover, input[type="submit"]:focus{
    background-color: rgba(255, 255, 255, 0.068);
    cursor: pointer;
}

@media (max-width: 768px){
    input[type="submit"]{
        width: 100%;
    }
}

#treeview .parent {
    position: relative;
}

#treeview .parent > ul {
    display: none;
}

#sticks {
  margin: 0vh 1vw;
  margin-bottom: 1vh;
  padding: 1vh 3vw;
  display: flex;
  flex-direction: column;
  border: 2px solid rgba(255, 255, 255, 0.11);
  border-radius: 20px;
  background-color: #161b22;
  align-items: center;
}

#sticks.stick {
  position: sticky;
  top: 0;
  z-index: 10000;
}
</style>
<script>
function s_validate() {
    if ($("input[name^='filenode_']:checked").length == 0) {
        alert("Select one file at least!");
        return false;
        }
    }
</script>
</head>
<body>
  <!--© Designed and coded by @KPSBots-Telegram-->
    <header>
      <div class="brand">
        <img
          src="https://graph.org/file/1a6ad157f55bc42b548df.png"
          alt="logo"
        />
        <a href="https://telegram.me/KPSBots">
          <h2 class="name">Bittorrent Selection</h2>
        </a>
      </div>
      <div class="social">
        <a href="https://github.com/Tamilupdates/KPSML-X"><i class="fab fa-github"></i></a>
        <a href="https://telegram.me/KPSBots"><i class="fab fa-telegram"></i></a>
      </div>
    </header>
    <div id="sticks">
        <h4>Selected files: <b id="checked_files">0</b> of <b id="total_files">0</b></h4>
        <h4>Selected files size: <b id="checked_size">0</b> of <b id="total_size">0</b></h4>
    </div>
      <section>
      <form action="{form_url}" onsubmit="return s_validate()" method="POST">
       {My_content}
       <input type="submit" name="Select these files ;)">
      </form>
    </section>

    <script>
      $(document).ready(function () {
        docready();
        var tags = $("li").filter(function () {
          return $(this).find("ul").length !== 0;
        });

        tags.each(function () {
          $(this).addClass("parent");
        });

        $("body").find("ul:first-child").attr("id", "treeview");
        $(".parent").prepend("<span>▶</span>");

        $("span").click(function (e) {
          e.stopPropagation();
          e.stopImmediatePropagation();
          $(this).parent( ".parent" ).find(">ul").toggle("slow");
          if ($(this).hasClass("active")) $(this).removeClass("active");
          else $(this).addClass("active");
        });
      });

      if(document.getElementsByTagName("ul").length >= 10){
        var labels = document.querySelectorAll("label");
        //Shorting the file/folder names
        labels.forEach(function (label) {
            if (label.innerText.toString().split(" ").length >= 9) {
                let FirstPart = label.innerText
                    .toString()
                    .split(" ")
                    .slice(0, 5)
                    .join(" ");
                let SecondPart = label.innerText
                    .toString()
                    .split(" ")
                    .splice(-5)
                    .join(" ");
                label.innerText = `${FirstPart}... ${SecondPart}`;
            }
            if (label.innerText.toString().split(".").length >= 9) {
                let first = label.innerText
                    .toString()
                    .split(".")
                    .slice(0, 5)
                    .join(" ");
                let second = label.innerText
                    .toString()
                    .split(".")
                    .splice(-5)
                    .join(".");
                label.innerText = `${first}... ${second}`;
            }
        });
    }
    </script>

<script>
$('input[type="checkbox"]').change(function(e) {
  var checked = $(this).prop("checked"),
      container = $(this).parent(),
      siblings = container.siblings();
/*
  $(this).attr('value', function(index, attr){
     return attr == 'yes' ? 'noo' : 'yes';
  });
*/
  container.find('input[type="checkbox"]').prop({
    indeterminate: false,
    checked: checked
  });
  function checkSiblings(el) {
    var parent = el.parent().parent(),
        all = true;
    el.siblings().each(function() {
      let returnValue = all = ($(this).children('input[type="checkbox"]').prop("checked") === checked);
      return returnValue;
    });

    if (all && checked) {
      parent.children('input[type="checkbox"]').prop({
        indeterminate: false,
        checked: checked
      });
      checkSiblings(parent);
    } else if (all && !checked) {
      parent.children('input[type="checkbox"]').prop("checked", checked);
      parent.children('input[type="checkbox"]').prop("indeterminate", (parent.find('input[type="checkbox"]:checked').length > 0));
      checkSiblings(parent);
    } else {
      el.parents("li").children('input[type="checkbox"]').prop({
        indeterminate: true,
        checked: false
      });
    }
  }
  checkSiblings(container);
});
</script>
<script>
    function docready () {
        $("label[for^='filenode_']").css("cursor", "pointer");
        $("label[for^='filenode_']").click(function () {
            $(this).prev().click();
        });
        checked_size();
        checkingfiles();
        var total_files = $("label[for^='filenode_']").length;
        $("#total_files").text(total_files);
        var total_size = 0;
        var ffilenode = $("label[for^='filenode_']");
        ffilenode.each(function () {
            var size = parseFloat($(this).data("size"));
            total_size += size;
            $(this).append(" - " + humanFileSize(size));
        });
        $("#total_size").text(humanFileSize(total_size));
    };
    function checked_size() {
        var checked_size = 0;
        var checkedboxes = $("input[name^='filenode_']:checked");
        checkedboxes.each(function () {
            var size = parseFloat($(this).data("size"));
            checked_size += size;
        });
        $("#checked_size").text(humanFileSize(checked_size));
    }
    function checkingfiles() {
        var checked_files = $("input[name^='filenode_']:checked").length;
        $("#checked_files").text(checked_files);
    }
    $("input[name^='foldernode_']").change(function () {
        checkingfiles();
        checked_size();
    });
    $("input[name^='filenode_']").change(function () {
        checkingfiles();
        checked_size();
    });
    function humanFileSize(size) {
        var i = -1;
        var byteUnits = [' kB', ' MB', ' GB', ' TB', 'PB', 'EB', 'ZB', 'YB'];
        do {
            size = size / 1024;
            i++;
        } while (size > 1024);
        return Math.max(size, 0).toFixed(1) + byteUnits[i];
    }
    function sticking() {
        var window_top = $(window).scrollTop();
        var div_top = $('.brand').offset().top;
        if (window_top > div_top) {
            $('#sticks').addClass('stick');
        } else {
            $('#sticks').removeClass('stick');
        }
    }
    $(function () {
        $(window).scroll(sticking);
        sticking();
    });
</script>
</body>
</html>
"""

code_page = """
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Torrent Code Checker</title>
    <link rel="icon" href="https://graph.org/file/1a6ad157f55bc42b548df.png" type="image/jpg">
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css"
      integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p"
      crossorigin="anonymous"
    />
    <style>
     *{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Ubuntu", sans-serif;
    list-style: none;
    text-decoration: none;
    color: white;
}

body{
    background-color: #0D1117;
}

header{
    margin: 3vh 1vw;
    padding: 0.5rem 1rem 0.5rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: #161B22;
    border-radius: 30px;
    background-color: #161B22;
    border: 2px solid rgba(255, 255, 255, 0.11);
}

header:hover, section:hover{
    box-shadow: 0px 0px 15px black;
}

.brand{
    display: flex;
    align-items: center;
}

img{
    width: 2.5rem;
    height: 2.5rem;
    border: 2px solid black;
    border-radius: 50%;
}

.name{
    color: white;
    margin-left: 1vw;
    font-size: 1.5rem;
}

.intro{
    text-align: center;
    margin-bottom: 2vh;
    margin-top: 1vh;
}

.social a{
    font-size: 1.5rem;
    color: white;
    padding-left: 1vw;
}

.social a:hover, .brand:hover{
    filter: invert(0.3);
}

section{
    margin: 0vh 1vw;
    margin-bottom: 10vh;
    padding: 1vh 3vw;
    display: flex;
    flex-direction: column;
    border: 2px solid rgba(255, 255, 255, 0.11);
    border-radius: 20px;
    background-color: #161B22 ;
    color: white;
}

section form{
    display: flex;
    margin-left: auto;
    margin-right: auto;
    flex-direction: column;
}

section div{
    background-color: #0D1117;
    border-radius: 20px;
    max-width: fit-content;
    padding: 0.7rem;
    margin-top: 2vh;
}

section label{
    font-size: larger;
    font-weight: 500;
    margin: 0 0 0.5vh 1.5vw;
    display: block;
}

section input[type="text"]{
    border-radius: 20px;
    outline: none;
    width: 50vw;
    height: 4vh;
    padding: 1rem;
    margin: 0.5vh;
    border: 2px solid rgba(255, 255, 255, 0.11);
    background-color: #3e475531;
    box-shadow: inset 0px 0px 10px black;
}

section input[type="text"]:focus{
    border-color: rgba(255, 255, 255, 0.404);
}

section button{
    border-radius: 20px;
    margin-top: 1vh;
    width: 100%;
    height: 5.5vh;
    border: 2px solid rgba(255, 255, 255, 0.11);
    background-color: #0D1117;
    color: white;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 200ms ease;
}

section button:hover, section button:focus{
    background-color: rgba(255, 255, 255, 0.068);
}

section span{
    display: block;
    font-size: x-small;
    margin: 1vh;
    font-weight: 100;
    font-style: italic;
    margin-left: 23%;
    margin-right: auto;
    margin-bottom: 2vh;
}

@media (max-width: 768px) {
    section form{
        flex-direction: column;
        width: 90vw;
    }

    section div{
        max-width: 100%;
        margin-bottom: 1vh;
    }

    section label{
        margin-left: 3vw;
        margin-top: 1vh;
    }

    section input[type="text"]{
        width: calc(100% - 0.3rem);
    }

    section button{
        width: 100%;
        height: 5vh;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    section span{
        margin-left: 5%;
    }
}
    </style>
  </head>
<body>
   <!--© Designed and coded by @KPSBots-Telegram-->
    <header>
      <div class="brand">
        <img
          src="https://graph.org/file/1a6ad157f55bc42b548df.png"
          alt="logo"
        />
        <a href="https://telegram.me/KPSBots">
          <h2 class="name">Bittorrent Selection</h2>
        </a>
      </div>
      <div class="social">
        <a href="https://github.com/Tamilupdates/KPSML-X"><i class="fab fa-github"></i></a>
        <a href="https://telegram.me/KPSBots"><i class="fab fa-telegram"></i></a>
      </div>
    </header>
    <section>
      <form action="{form_url}">
        <div>
          <label for="pin_code">Pin Code :</label>
          <input
            type="text"
            name="pin_code"
            placeholder="Enter the code that you have got from Telegram to access the Torrent"
          />
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
          <span
            >* Dont mess around. Your download will get messed up.</
          >
    </section>
</body>
</html>
"""


def re_verfiy(paused, resumed, client, hash_id):

    paused = paused.strip()
    resumed = resumed.strip()
    if paused:
        paused = paused.split("|")
    if resumed:
        resumed = resumed.split("|")

    k = 0
    while True:
        res = client.torrents_files(torrent_hash=hash_id)
        verify = True
        for i in res:
            if str(i.id) in paused and i.priority != 0:
                verify = False
                break
            if str(i.id) in resumed and i.priority == 0:
                verify = False
                break
        if verify:
            break
        LOGGER.info("Reverification Failed! Correcting stuff...")
        client.auth_log_out()
        sleep(1)
        client = qbClient(host="localhost", port="8090")
        try:
            client.torrents_file_priority(
                torrent_hash=hash_id, file_ids=paused, priority=0)
        except NotFound404Error as e:
            raise NotFound404Error from e
        except Exception as e:
            LOGGER.error(f"{e} Errored in reverification paused!")
        try:
            client.torrents_file_priority(
                torrent_hash=hash_id, file_ids=resumed, priority=1)
        except NotFound404Error as e:
            raise NotFound404Error from e
        except Exception as e:
            LOGGER.error(f"{e} Errored in reverification resumed!")
        k += 1
        if k > 5:
            return False
    LOGGER.info(f"Verified! Hash: {hash_id}")
    return True


@app.route('/app/files/<string:id_>', methods=['GET'])
def list_torrent_contents(id_):

    if "pin_code" not in request.args.keys():
        return code_page.replace("{form_url}", f"/app/files/{id_}")

    pincode = ""
    for nbr in id_:
        if nbr.isdigit():
            pincode += str(nbr)
        if len(pincode) == 4:
            break
    if request.args["pin_code"] != pincode:
        return "<h1>Incorrect pin code</h1>"

    if len(id_) > 20:
        client = qbClient(host="localhost", port="8090")
        res = client.torrents_files(torrent_hash=id_)
        cont = make_tree(res)
        client.auth_log_out()
    else:
        res = aria2.client.get_files(id_)
        cont = make_tree(res, True)
    return page.replace("{My_content}", cont[0]).replace("{form_url}", f"/app/files/{id_}?pin_code={pincode}")


@app.route('/app/files/<string:id_>', methods=['POST'])
def set_priority(id_):

    data = dict(request.form)
    resume = ""
    if len(id_) > 20:
        pause = ""

        for i, value in data.items():
            if "filenode" in i:
                node_no = i.split("_")[-1]

                if value == "on":
                    resume += f"{node_no}|"
                else:
                    pause += f"{node_no}|"

        pause = pause.strip("|")
        resume = resume.strip("|")

        client = qbClient(host="localhost", port="8090")

        try:
            client.torrents_file_priority(
                torrent_hash=id_, file_ids=pause, priority=0)
        except NotFound404Error as e:
            raise NotFound404Error from e
        except Exception as e:
            LOGGER.error(f"{e} Errored in paused")
        try:
            client.torrents_file_priority(
                torrent_hash=id_, file_ids=resume, priority=1)
        except NotFound404Error as e:
            raise NotFound404Error from e
        except Exception as e:
            LOGGER.error(f"{e} Errored in resumed")
        sleep(1)
        if not re_verfiy(pause, resume, client, id_):
            LOGGER.error(f"Verification Failed! Hash: {id_}")
        client.auth_log_out()
    else:
        for i, value in data.items():
            if "filenode" in i and value == "on":
                node_no = i.split("_")[-1]
                resume += f'{node_no},'

        resume = resume.strip(",")

        res = aria2.client.change_option(id_, {'select-file': resume})
        if res == "OK":
            LOGGER.info(f"Verified! GID: {id_}")
        else:
            LOGGER.info(f"Verification Failed! Report! GID: {id_}")
    return list_torrent_contents(id_)



@app.route('/<string:id_>', methods=['GET'])
def stream_video(id_):
    return f'''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Professional Stream Engine 3.0</title>
        <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
        <link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet" />
        <style>
            body {{
                background-color: #1A2238;
                color: #FFFFFF;
                font-family: 'Ubuntu', sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
            }}
            .header {{
                background-color: #111726;
                padding: 15px 20px;
                border-bottom: 2px solid #FF9E6D;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }}
            .header h2 {{ margin: 0; font-size: 20px; color: #FFFFFF; }}
            .container {{ max-width: 900px; margin: 30px auto; padding: 20px; }}
            .video-container {{
                width: 100%;
                background-color: #000;
                border: 2px solid #FF9E6D;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 8px 16px rgba(255, 158, 109, 0.2);
                margin-bottom: 30px;
            }}
            .btn-container {{
                display: flex;
                flex-direction: column;
                gap: 15px;
                align-items: center;
                margin-bottom: 30px;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #FF9E6D;
                color: #1A2238;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                transition: all 0.3s ease;
                width: 80%;
                max-width: 300px;
                border: 2px solid transparent;
            }}
            .btn:hover {{
                background-color: transparent;
                color: #FF9E6D;
                border-color: #FF9E6D;
                box-shadow: 0 0 10px rgba(255, 158, 109, 0.5);
            }}
            .btn-secondary {{
                background-color: #2c3a60;
                color: #FFFFFF;
                border: 2px solid transparent;
            }}
            .btn-secondary:hover {{
                background-color: transparent;
                color: #FFFFFF;
                border-color: #2c3a60;
                box-shadow: 0 0 10px rgba(44, 58, 96, 0.5);
            }}
            .track-box {{
                background-color: #111726;
                padding: 20px;
                border-radius: 12px;
                text-align: left;
                border: 1px solid rgba(255, 158, 109, 0.3);
            }}
            .track-box h3 {{
                color: #FF9E6D;
                margin-top: 0;
                border-bottom: 1px solid rgba(255, 158, 109, 0.3);
                padding-bottom: 10px;
            }}
            .track-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            .track-item:last-child {{
                border-bottom: none;
            }}
            .btn-small {{
                padding: 8px 16px;
                font-size: 14px;
                width: auto;
                margin: 0;
            }}

            /* Customizing Plyr for Theme */
            .plyr--video .plyr__control--overlaid {{
                background: rgba(255, 158, 109, 0.8);
            }}
            .plyr--video .plyr__control.plyr__tab-focus,
            .plyr--video .plyr__control:hover,
            .plyr--video .plyr__control[aria-expanded=true] {{
                background: #FF9E6D;
            }}
            .plyr__control--overlaid:focus, .plyr__control--overlaid:hover {{
                background: #FF9E6D;
            }}
            .plyr--full-ui input[type=range] {{
                color: #FF9E6D;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>Professional Stream Engine 3.0</h2>
            <div style="font-size: 14px; color: #aaa;">ID: {{id_}}</div>
        </div>

        <div class="container">
            <h3 style="color: #FF9E6D; margin-bottom: 20px;">Now Playing</h3>

            <div class="video-container">
                <video id="player" playsinline controls data-poster="https://graph.org/file/0ff9d5e94a070fe4154c0.jpg">
                    <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" type="video/mp4" />
                </video>
            </div>

            <div class="btn-container">
                <a href="/download/{{id_}}" class="btn">Download Full Video</a>
                <a href="https://t.me/SECRECT_BOT_UPDATES" class="btn btn-secondary">Support Group</a>
            </div>

            <div class="track-box">
                <h3>TRACK EXTRACTION CENTER</h3>
                <p style="font-size: 14px; color: #bbb; font-style: italic; margin-bottom: 15px;">Note: Direct streaming backend is using a placeholder. Metadata extraction requires downloading the file.</p>

                <div class="track-item">
                    <span>Audio Track 1 (hin)</span>
                    <a href="#" class="btn btn-secondary btn-small">Extract MP3</a>
                </div>

                <div class="track-item">
                    <span>Subtitle 1 (eng)</span>
                    <a href="#" class="btn btn-secondary btn-small">Extract ASS</a>
                </div>
            </div>
        </div>

        <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
        <script>
            const player = new Plyr('#player', {{
                title: 'Video Player',
                controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'captions', 'settings', 'pip', 'airplay', 'fullscreen'],
            }});
        </script>
    </body>
    </html>
    '''


@app.route('/download/<string:id_>', methods=['GET'])
def download_file(id_):
    path = id_
    if not path:
        return "Missing path parameter", 400
    return f"<h1>Download requested for ID: {path}</h1><p>Note: Direct downloading from Telegram requires a streaming backend not present in this bot.</p>"

@app.route('/')
def homepage():
    return """
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link
      href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap"
      rel="stylesheet"
    />
    <style>
        body {
            background-color: #0D1117;
            color: white;
            font-family: "Ubuntu", sans-serif;
        }
        .header {
            background-color: black;
            text-align: center;
            width: 100%;
            padding: 1px;
        }
        .footer {
            background-color: black;
            padding: 10px;
            text-align: center;
            position: absolute;
            bottom: 0;
            width: 100%;
        }
        .content {
            padding: 20px;
            text-align: center;
        }
        .button {
            background-color: #0001f0;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .image {
            border-radius: 12px;
            max-width: 100%;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>KPSML-X</h1>
    </div>
    <div class="content">
        <img src="https://graph.org/file/0ff9d5e94a070fe4154c0.jpg" class="image">
        <a href="https://telegram.me/KPSBots" style="text-decoration: none;">
            <button class="button">Join Updates Channel Now</button>
        </a>
    </div>
    <div class="footer">
&copy; <script>document.write(new Date().getFullYear() + '-' + String(new Date().getFullYear() + 1).slice(-2));</script> KPSML-X. All Rights Reserved.
    </div>
</body>
</html>
"""


@app.errorhandler(Exception)
def page_not_found(e):
    return f"<h1>404: Torrent not found! Mostly wrong input. <br><br>Error: {e}</h2>", 404


if __name__ == "__main__":
    app.run()
