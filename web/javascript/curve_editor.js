var CurveEditor = {

    methods: {
        drawGrid: function() {
            var ctx = this.curve_canvas.getContext("2d");
            ctx.save();

            ctx.fillStyle="#212121";
            ctx.fillRect( 0,0, this.curve_canvas.width, this.curve_canvas.height );
            ctx.lineWidth = 0.5;

            ctx.strokeStyle = "#010101";
            ctx.setLineDash( [1,3] );
            ctx.beginPath();
            grid_pos = -1.0;
            while(grid_pos <1.0) {
                var realX = (grid_pos+1.0) * this.width;
                ctx.moveTo( realX, 0 );
                ctx.lineTo( realX, this.height );
                ctx.stroke();
                grid_pos += this.grid_unit;
            }

            grid_pos = -1.0;
            while(grid_pos <1.0) {
                var realY = (grid_pos+1.0) * this.height;
                ctx.moveTo( 0, realY );
                ctx.lineTo( this.width, realY );
                ctx.stroke();
                grid_pos += this.grid_unit;
            }

            ctx.setLineDash([]);
            ctx.strokeStyle = "#DDDDDD";
            ctx.beginPath();
            ctx.moveTo( this.center_x, 0 );
            ctx.lineTo( this.center_x, this.height );
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo( 0, this.center_y );
            ctx.lineTo( this.width, this.center_y );
            ctx.stroke();

            ctx.strokeStyle = "#010101";
            ctx.lineWidth = 0.75;
            ctx.setLineDash( [3,1] );
            ctx.beginPath();
            var innerWidth = this.width - (this.margin_ratio* this.width*2);
            var innerHeight = this.height - (this.margin_ratio* this.height*2);

            ctx.strokeRect( 0 + this.margin_ratio*this.width, 
                            0 + this.margin_ratio*this.height,
                            innerWidth,
                            innerHeight );

            ctx.restore();
        
        },

        setPoints: function() {

        },

        drawTimeline: function() {
            var ctx = this.timeline_canvas.getContext("2d");
            ctx.save();
            ctx.fillStyle="#AFAFAF";
            ctx.fillRect( 0,0, this.timeline_canvas.width, this.timeline_canvas.height );

            var l = this.getLength();
            var ticks = l * 60;
            
            for(var i=0; i<ticks; ++i) {
                var realX = i * this.timeline_canvas.width / ticks;
                ctx.moveTo( realX, 0 );
    
                if(i%this.fps == 0) {
                    ctx.lineTo( realX, this.timeline_canvas.height/2 );
                } else {
                    if(i%5 ==0) {
                        ctx.lineTo( realX, this.timeline_canvas.height/3 );
                    }
                }
                ctx.stroke();
            }

            ctx.restore();
        },

        getLength: function() {
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
            this.points = [];
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

    _.each( _.keys( CurveEditor.methods),(key)=> {
        owner["CurveEditor"][key] = CurveEditor.methods[key];
    });
    owner.CurveEditor.initialize();
}
