
function remote_python( code, callback ) {

    var deferred = new $.Deferred();
    var bgl_request = {
        api_key: "Eikaipoothering9kijobei7Ley9coo5",
        python: code
    };
    $.get("/api/?" + encodeURIComponent(JSON.stringify(bgl_request)), callback );
}

function editor_init() {
    //$("#run_test").click( ()=>{
    //    remote_python( "self.get_version_info()", (data)=>{ console.log(data); });
    //})

    $.get("/frontend/html/curve_editor.html", (data) => { $("#activeEditor").html(data) } );
}
