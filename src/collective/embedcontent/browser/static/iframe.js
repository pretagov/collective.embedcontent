 $(document).ready(function () {
        $("iframe.embed-content-frame").on( "load", function () {
          $(this).height($(this).contents().find("html").height());
      });
    });
