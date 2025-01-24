import threading

from fastapi import FastAPI
import gpxpy
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
from fastapi.responses import JSONResponse
import uvicorn
app = FastAPI()



# Открываем GPX файл
gpx_file = "00000002.BIN.gpx"
with open(gpx_file, "r") as file:
    gpx = gpxpy.parse(file)

# Пример: Преобразование точек треков в GeoDataFrame
track_points = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            track_points.append({
                "geometry": Point(point.longitude, point.latitude),
                "elevation": point.elevation,
                "time": point.time
            })

gdf = gpd.GeoDataFrame(track_points, crs="EPSG:4326")

df = pd.read_csv('2023-06-30_11-54-52.txt', sep=' ')

print(gdf.info())
print(df.info())


@app.get("/")
async def root():
    return {"message": "interview test service"}


@app.get("/getPos")
async def get_data(limit: int = 10, start: int = 0):
    currentLimit = limit if limit < 100 else 100
    print(currentLimit)
    currentStartRecord = start if start < len(df)-currentLimit else len(df)-currentLimit
    return {"data":"coordinates",
            "totalrows": len(df),
            "limit": currentLimit,
            "start": currentStartRecord,
            "records": [{"time": record.time, "lon": record.geometry.x-0.5, "lat": record.geometry.y-0.5 } for 
                        record in gdf.iloc[currentStartRecord:currentStartRecord+currentLimit].itertuples(index=False)]}

@app.get("/getData")
async def get_data(limit: int = 10, start: int = 0):
    currentLimit = limit if limit < 100 else 100
    currentStartRecord = start if start < len(df)-currentLimit else len(df)-currentLimit
    return {"data":"values",
            "totalrows": len(df),
            "limit": currentLimit,
            "start": currentStartRecord,
            "records": [{"value": record.Val, "date": record.DATE, "time": record.TIME } for 
                        record in df.iloc[currentStartRecord:currentStartRecord+currentLimit].itertuples(index=False)]}

def run_server(server: uvicorn.Server):
    server.run()

if __name__ == "__main__":
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server_thread = threading.Thread(target=run_server, args=(server, ))
    server_thread.start()
