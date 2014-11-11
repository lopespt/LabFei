var environments = {
	production : 0,
	testing : 1
};
var serviceUrls = [ "ws://labfei.gwachs.com/CorrectionService",
		"ws://localhost:8080/LabFEI/CorrectionService" ];


//Set the environment
var environment = environments.testing;



var labService;
$(document)
		.ready(
				function() {

					labService = {
						submission : 0,
						socket : null,

						sendLab : function() {
							labService.socket = new WebSocket(
									serviceUrls[environment]);
							labService.socket.onmessage = function(msg) {
								// console.dir(msg);
								message = msg.data;
								if (message == "update") {
									labService.refreshResults();
								}
							}

							form = $("#formDetails").ajaxForm();
							form
									.ajaxSubmit({
										error : function(xhr, txtStatus,
												errorThrown) {
											alert("Ocorreu um erro no envio dos arquivos: "
													+ errorThrown);
										},
										success : function(json) {
											labService.submission = json;
											labService.registerListener();
										}
									});

						},

						refreshResults : function() {
							$.ajax({
								url : "results",
								type : "post",
								success : function(html) {
									$("#results").html(html);
								}
							})
						},

						registerListener : function() {
							// socket.onopen = function() {
							labService.socket.send(JSON
									.stringify(labService.submission));
							// alert("Conexao aberta!");
							// }

						}

					};

					$("#but_send").click(function() {
						alert("Vou enviar");
						labService.sendLab();
					});

					labService.refreshResults();
				});