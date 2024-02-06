// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

$(function () {
  var reportContainer = $("#report-container").get(0);

  // Initialize iframe for embedding report
  powerbi.bootstrap(reportContainer, { type: "report" });

  var models = window["powerbi-client"].models;
  var reportLoadConfig = {
      type: "report",
      tokenType: models.TokenType.Embed,
      settings: {
          bars: {
              statusBar: {
                  visible: true
              }
          },
          filterPaneEnabled: false
      }

      // Enable this setting to remove gray shoulders from embedded report
      // settings: {
      //     background: models.BackgroundType.Transparent
      // }
  };

  $.ajax({
      type: "GET",
      url: $("body").attr("data-base-url") + "/getembedinfo",
      dataType: "json",
      success: function (data) {
          result = $.parseJSON(JSON.stringify(data));
          embedData = result['embed'];
          filters = result['filters']

          reportLoadConfig.accessToken = embedData.accessToken;

          // You can embed different reports as per your need
          reportLoadConfig.embedUrl = embedData.reportConfig[0].embedUrl;

          // Use the token expiry to regenerate Embed token for seamless end user experience
          // Refer https://aka.ms/RefreshEmbedToken
          tokenExpiry = embedData.tokenExpiry;

          // Embed Power BI report when Access token and Embed URL are available
          var report = powerbi.embed(reportContainer, reportLoadConfig);

          // Triggers when a report schema is successfully loaded
          report.on("loaded", async function () {
            console.log("Report load successful")

            // Pages
            var pages = await report.getPages();
            console.log("Pages")
            console.log(pages);

            if (filters['page'] !== null && filters['page'] !== "") {
              const p = pages.find(b => b.displayName === filters['page'])
              console.log("Page")
              console.log(p)
              await report.setPage(p.name);

              // Visuals
              var visuals = await p.getVisuals();
              const visuals_slicers = visuals.filter(b => b.type === 'slicer')
              console.log("Slicers");
              console.log(visuals_slicers);

              var filters_data = [];

              if (filters['search_key_1'] !== null && filters['search_key_1'] !== "") {
                const f = await visuals_slicers.find(b => b.title === filters['search_key_1']).getFilters();
                console.log("Visuals " + filters['search_key_1']);
                console.log(f[0]);

                filters_data.push(
                  {
                    $schema: "http://powerbi.com/product/schema#basicFilter",
                    target: {
                      table: f[0].target.table,
                      column: f[0].target.column
                    },
                    operator: "In",
                    values: filters['search_value_1']
                  }
                );
              }

              if (filters['search_key_2'] !== null && filters['search_key_2'] !== "") {
                const f = await visuals_slicers.find(b => b.title === filters['search_key_2']).getFilters();
                console.log("Visuals " + filters['search_key_2']);
                console.log(f[0]);

                filters_data.push(
                  {
                    $schema: "http://powerbi.com/product/schema#basicFilter",
                    target: {
                      table: f[0].target.table,
                      column: f[0].target.column
                    },
                    operator: "In",
                    values: filters['search_value_2']
                  }
                );
              }

              // Aplicar los filtros según el nivel (report, page, visual)
              console.log("Filters");
              console.log(filters_data);
              report.setFilters(filters_data).catch(error => console.error("Error " + error));
            }
          });

          // Triggers when a report is successfully embedded in UI
          report.on("rendered", function () {
              console.log("Report render successful")
          });

          // Clear any other error handler event
          report.off("error");

          // Below patch of code is for handling errors that occur during embedding
          report.on("error", function (event) {
              var errorMsg = event.detail;

              // Use errorMsg variable to log error in any destination of choice
              console.error(errorMsg);
              return;
          });
      },
      error: function (err) {

          // Show error container
          var errorContainer = $(".error-container");
          $(".embed-container").hide();
          errorContainer.show();

          // Format error message
          var errMessageHtml = "<strong> Error Details: </strong> <br/>" + $.parseJSON(err.responseText)["errorMsg"];
          errMessageHtml = errMessageHtml.split("\n").join("<br/>")

          // Show error message on UI
          errorContainer.html(errMessageHtml);
      }
  });
});