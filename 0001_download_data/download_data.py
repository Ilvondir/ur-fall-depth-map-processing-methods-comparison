from pathlib import Path
import requests
import tqdm
from zipfile import ZipFile



FALL_SEQUENCES = 30
ADL_SEQUENCES = 40

path = Path('datasets')
path.mkdir(exist_ok=True)

for label in ['fall', 'adl']:
    for i in tqdm.tqdm(range(1, (FALL_SEQUENCES+1) if label == 'fall' else ADL_SEQUENCES+1)):
        url = f'https://fenix.ur.edu.pl/~mkepski/ds/data/{label}-{i:02}-cam0-d.zip'
        response = requests.get(url)

        if response.status_code == 200:
            zip_path = path / f'{label}-{i:02}.zip'
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            
            output_path = path / label / f'sequence-{i:02}'
            output_path.mkdir(exist_ok=True, parents=True)

            with ZipFile(zip_path, 'r') as zip:
                zip.extractall(output_path)
            
            zip_path.unlink()

            wrong_path = [f for f in output_path.iterdir() if f.is_dir()][0]
            for item in wrong_path.iterdir():
                target = output_path / item.name
                item.rename(target)

            wrong_path.rmdir()
