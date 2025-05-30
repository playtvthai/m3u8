document.addEventListener("DOMContentLoaded", function () {
const currentLocation = window.location.search;
const sURL = currentLocation.replace("?m=1&zy=", ""); 
  var tsPlayer = null,
      hlsPlayer = null,
      dashPlayer = null;

  var stopPlayers = function () {
    if (tsPlayer) {
      tsPlayer.destroy();
      tsPlayer = null;
    }

    if (hlsPlayer) {
      hlsPlayer.destroy();
      hlsPlayer = null;
    }

    if (dashPlayer) {
      dashPlayer.destroy();
      dashPlayer = null;
    }
  };

  var hide_for_error = function () {
    $("#player").hide();
    stopPlayers();
  };

  var show_for_ok = function () {
    $("#player").show();
  };

  // Start play HTTP-TS.
  if (!window.mpegts) {
    mpegts.LoggingControl.applyConfig({
      enableDebug: false,
      enableVerbose: false,
      enableInfo: false,
      enableWarn: false,
      enableError: true
    });
    hide_for_error();
    return;
  }

  show_for_ok();

  tsPlayer = videojs("#player");
  tsPlayer.src({
    src: sURL,
    type: "video/mp2t",
    suppressNotSupportedError: true,
    mediaDataSource: {
      type: "mpegts",
      isLive: true,
      cors: true,
      withCredentials: false
    },
    config: {
      enableWorker: true,
      enableWorkerForMSE: true
    }
  });

  tsPlayer.load();
  tsPlayer.play();
  //return;
  //}

  // Start play HLS.
  if (sURL.indexOf(".m3u8") > 0) {
    show_for_ok();

    hlsPlayer = new videojs("#player");
    hlsPlayer.src({
      type: "application/x-mpegURL",
      src: sURL
    });
    hlsPlayer.load();
    hlsPlayer.play();
    return;
  }

  // Start play MPEG-DASH.
  if (sURL.indexOf(".mpd") > 0) {
    show_for_ok();

    dashPlayer = new videojs("#player");
    dashPlayer.src({
      type: "application/dash+xml",
      src: sURL
    });
    dashPlayer.load();
    dashPlayer.play();
    return;
  }
});
