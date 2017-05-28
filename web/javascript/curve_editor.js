var CurveEditor = {

    ui_state: {
        mousedown: false
    },

    ui_events: {
        "curve_canvas" : { 
            "dblclick" : function(e) {
                coords = canvas_cursor_pos( this.curve_canvas, e );
                var glyphX = (coords.x / ( this.timeline_canvas.width - (this.timeline_canvas.width*this.margin_ratio*2))) + this.margin_ratio;
                var glyphY = (coords.y / ( this.timeline_canvas.height - (this.timeline_canvas.height*this.margin_ratio*2))) + this.margin_ratio;

                this.points.push({
                    "t" : this.t,
                    "vec" : [ glyphX, glyphY ]
                });

                this.points = _.sortBy( this.points, (pt) =>{ return pt.t } );
                },
        },

        "timeline_canvas" : {
            "mousedown" : function(e) {
                coords = canvas_cursor_pos( this.timeline_canvas, e );
                var normalT = (coords.x / this.timeline_canvas.width) * this.getLengthSeconds();
                this.setTime( normalT );
                this.ui_state.mousedown = true;
            },
            "mouseup" : function(e) {
                this.ui_state.mousedown = false;
            },
            "mouseleave" : function(e) {
                this.ui_state.mousedown = false;
            },
            "mousemove" : function(e) {
                if(this.ui_state.mousedown) {
                    coords = canvas_cursor_pos( this.timeline_canvas, e );
                    var normalT = (coords.x / this.timeline_canvas.width) * this.getLengthSeconds();
                    this.setTime( normalT );
                }
            }
         }
    },

    methods: {
        setTime: function( timeSec ) {
            this.t = timeSec;
            this.drawTimeline();

            this._timeline_synch += 1;
            var sequence = this._timeline_synch;
            var editor = this;
            remote_call_child( "eval_curve", { "t": this.t, "points" : this.points }, (data)=>{
                if( _.isArray( data.value ) ) {
                    if( editor._timeline_synch == sequence ) {
                        editor.glyphPosition.x = data.value[0];
                        editor.glyphPosition.y = data.value[1];
                        editor.drawGrid();
                    }
                }
            });
        },

        drawGrid: function() {
            var ctx = this.curve_canvas.getContext("2d");
            ctx.save();


            ctx.fillStyle="#012021";
            ctx.fillRect( 0,0, this.curve_canvas.width, this.curve_canvas.height );
            ctx.lineWidth = 1.0;

            ctx.font ="60px monospace";
            ctx.beginPath();
            ctx.strokeText( Math.round(this.t*this.fps) + "fr", 30, 60 );
            ctx.closePath();

            ctx.strokeStyle = "#010101";
            ctx.setLineDash( [1,3] );
            grid_pos = -1.0;
            while(grid_pos <1.0) {
                ctx.beginPath();
                var realX = (grid_pos+1.0) * this.width;
                ctx.moveTo( realX, 0 );
                ctx.lineTo( realX, this.height );
                ctx.stroke();
                grid_pos += this.grid_unit;
                ctx.closePath();
            }
            

            grid_pos = -1.0;
            while(grid_pos <1.0) {
                ctx.beginPath();
                var realY = (grid_pos+1.0) * this.height;
                ctx.moveTo( 0, realY );
                ctx.lineTo( this.width, realY );
                ctx.stroke();
                grid_pos += this.grid_unit;
                ctx.closePath();
            }

            ctx.setLineDash([]);
            ctx.strokeStyle = "#DDDDDD";
            ctx.beginPath();
            ctx.moveTo( this.center_x, 0 );
            ctx.lineTo( this.center_x, this.height );
            ctx.stroke();
            ctx.closePath();

            ctx.beginPath();
            ctx.moveTo( 0, this.center_y );
            ctx.lineTo( this.width, this.center_y );
            ctx.stroke();
            ctx.closePath();

            ctx.strokeStyle = "#010101";
            ctx.lineWidth = 0.75;
            ctx.setLineDash( [3,1] );
            var innerWidth = this.width - (this.margin_ratio* this.width*2);
            var innerHeight = this.height - (this.margin_ratio* this.height*2);

            ctx.strokeRect( 0 + this.margin_ratio*this.width, 
                            0 + this.margin_ratio*this.height,
                            innerWidth,
                            innerHeight );



            var realGlyphX = (this.glyphPosition.x / ( this.view[0] - this.view[0]*this.margin_ratio ) * this.curve_canvas.width ) + (this.curve_canvas.width / 2.0 );
            var realGlyphY = (this.glyphPosition.y / ( this.view[1] - this.view[1]*this.margin_ratio ) * this.curve_canvas.height) + (this.curve_canvas.height / 2.0 );

            ctx.fillStyle = "#FF00FF";
            ctx.fillRect( realGlyphX - 8, realGlyphY - 8, 16, 16 );

            ctx.restore();
        
        },

        setPoints: function() {

        },

        drawTimeline: function() {
            var ctx = this.timeline_canvas.getContext("2d");
            ctx.save();
            ctx.fillStyle="#1F2F1F";
            ctx.fillRect( 0,0, this.timeline_canvas.width, this.timeline_canvas.height );

            /*** ticks ***/
            var l = this.getLengthSeconds();
            var ticks = l * 60;
            
            ctx.strokeStyle="#FF0000";
            for(var i=0; i<ticks; ++i) {
                var realX = i * this.timeline_canvas.width / ticks;
    
                if(i%this.fps == 0) {
                    ctx.beginPath();
                    ctx.moveTo( realX, 0 );
                    ctx.lineTo( realX, this.timeline_canvas.height/2 );
                    ctx.stroke();
                    ctx.closePath();
                } else {
                    if(i%5 ==0) {
                        ctx.beginPath();
                        ctx.moveTo( realX, 0 );
                        ctx.lineTo( realX, this.timeline_canvas.height/3 );
                        ctx.stroke();
                        ctx.closePath();
                    }
                }
            }
            
            /*** keyframes ***/
            ctx.fillStyle = "#00FF00";
            _.each( this.points, (point)=>{ 
                var realX = this.timeline_canvas.width * (point.t/this.getLengthSeconds());
                ctx.fillRect( realX - this.keyframe_width, 0, this.keyframe_width*2, this.timeline_canvas.height * 0.75 );
            });

            /*** current time ***/
            var realTimeX = (this.t/this.getLengthSeconds()) * this.timeline_canvas.width;

            ctx.strokeStyle = "#0000FF";
            ctx.lineWidth = 3.0;
            ctx.setLineDash([1,1]);
            ctx.beginPath();
            ctx.moveTo( realTimeX, 0);
            ctx.lineTo( realTimeX, this.timeline_canvas.height ); 
            ctx.stroke();
            ctx.closePath();

            ctx.restore();
        },

        getLengthSeconds: function() {
            var length = 0.0;
            _.each( this.points, (point) => {
                if(point.t > length)
                    length = point.t;
            });
            return length;
        },

        setPoints: function(points) {
            this.points = points;
        },

        initialize: function() {
            this.curve_canvas = $(this.el).find(".curveEditorCanvas")[0];
            this.timeline_canvas = $(this.el).find(".curveEditorTimelineCanvas")[0];

            this.width = this.curve_canvas.width;
            this.height = this.curve_canvas.height;
            this.center_x = this.width/2;
            this.center_y = this.height/2;
            this.margin_ratio = 0.1;
            this.view = [ 16, 9 ];
            this.fps = 60;
            this.grid_unit = 0.05;
            this.keyframe_width = 5;
            this.t = 0.0;
            this.points = [];

            this._timeline_synch = 0; // used to line up network events
            this.glyphPosition = { "x" : 0.0, "y" : 0.0 };

            this.setPoints([{"t":0.0,"vec":[ 5.0,0.0]},{"t":10.0,"vec":[-5.0,0.0]}]);
            this.drawGrid();
            this.drawTimeline();
        }
    }
};

function curve_editor_init(id) {
    owner = $(id)[0];
    owner.CurveEditor = {};
    owner.CurveEditor.el = owner;
    owner.CurveEditor.ui_state = {};

    _.each( _.keys( CurveEditor.methods),(key)=> {
        owner["CurveEditor"][key] = CurveEditor.methods[key];
    });

    _.each( _.keys( CurveEditor.ui_state),(key)=> {
        owner["CurveEditor"]["ui_state"][key] = CurveEditor.ui_state[key];
    });

    owner.CurveEditor.initialize();

    _.each( _.keys( CurveEditor.ui_events), (widget)=> {
        _.each( _.keys( CurveEditor.ui_events[widget]) , (event_name) => {
            $(owner.CurveEditor[widget])[event_name]( _.bind( CurveEditor.ui_events[widget][event_name], owner.CurveEditor ));
        });
    });
}
