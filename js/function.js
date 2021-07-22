function scaleMe(data) {
    var start = data.start,
        hours = Math.floor(start.valueOf() / 3600000) % 24,
        ampm = ["am", "pm"][Math.floor(hours / 12)],
        hh = ((hours - 24) % 12) + 12;

    return hh + ampm;
}

function makeDate(sDate) {
    var adjusted = sDate.replace(/^([0-9]{4})-([0-9]{2})-([0-9]{2}).([0-9]{2}):([0-9]{2}):([0-9]{2})$/, "$1/$2/$3 $4:$5:$6");

    return new Date(adjusted);
}

function process(netResponse) {
    var list = netResponse.json(),
        i = list.length,
        services = {},
        programmes = null,
        latest = new Date(0),
        earliest = new Date("2099/12/31 23:59:59"),
        thisStart = null,
        thisEnd = null,
        thisService = null;

    // grab required tracks and transform items
    while (i--) {
        thisService = list[i].service;
        services[thisService] = services[thisService] || {title: list[i].service_title, programmes: []};
        programmes = services[thisService].programmes;

        thisStart = makeDate(list[i].start);
        thisEnd = makeDate(list[i].end);

        // deduce required Timetable end points
        if(thisStart.valueOf() < earliest.valueOf()) {
            earliest = thisStart;
        }

        if(thisEnd.valueOf() > latest.valueOf()) {
            latest = thisEnd;
        }

        programmes[programmes.length] = [
            list[i].emp_title,
            thisStart,
            thisEnd
        ];
    }

    // deduce required Timetable view points
//    var viewStart = new Date(earliest.valueOf() + 3 * 60 * 60 * 1000),
//        viewEnd = new Date(earliest.valueOf() + 6 * 60 * 60 * 1000),
    var viewStart = earliest,
        viewEnd = latest,
        tracks = []
        trackSize = 155;

    // transform grabbed tracks
    for(var id in services) {
        tracks[tracks.length] = [services[id].title, trackSize, {items: services[id].programmes}];
    }

    // disable all tracks but the first 4. tracks[j][2] is the options object
    // this is so we have something that fits the page
    /*for(var j = 4, len = tracks.length; j < len; j++) {
        tracks[j][2].disabled = true;
    }*/
    
//		console.log({
//			tracks: tracks,
//			earliest: earliest,
//			latest: latest,
//			viewStart: viewStart,
//			viewEnd: viewEnd
//		});
    
    return {
        tracks: tracks,
        earliest: earliest,
        latest: latest,
        viewStart: viewStart,
        viewEnd: viewEnd
    };
}