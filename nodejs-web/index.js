const express = require('express');
const multer = require('multer');
const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

// Set up multer for file uploads with the original file name
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
});

const upload = multer({ storage: storage });

// Parse URL-encoded bodies (as sent by HTML forms)
app.use(express.urlencoded({ extended: true }));

// Serve static files from the "public" directory
app.use(express.static('public'));

// 각 디렉토리 경로 연결
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
app.use('/result', express.static(path.join(__dirname, 'result')));
app.use('/sample', express.static(path.join(__dirname, 'sample')));

// 이미지 업로드 및 분석 기능
app.post('/upload', upload.single('image'), (req, res) => {
    const test_img = path.join(__dirname, req.file.path);

    // 모델 경로 및 파이썬 경로 가져오기
    const model_path = path.join(__dirname, '../python-script/model/train/old-cell.pt');
    const scriptPath = path.join(__dirname, '../python-script/run_segmentation.py');

    // 가상환경 연결 (다른 컴퓨터에서는 본인 python환경으로 수정 필요)
    const pythonExecutable = '/Users/seoseondeok/miniconda3/envs/yolov8/bin/python';

    // 픽셀당 실제길이 값 처리여부 확인
    const pixelToReal = req.body.pixelToReal;
    const unit = req.body.unit;
    const noPixelReal = req.body.noPixelReal === 'on';  // 'on' means checked

    // Construct the arguments for the Python script
    const args = [scriptPath, test_img, model_path];

    if (!noPixelReal && pixelToReal) {
        args.push(pixelToReal);
    }

    // 연결한 가상환경과 python-script에 있는 코드 실행
    execFile(pythonExecutable, args, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${stderr}`);
            return res.status(500).json({ error: 'Segmentation failed.' });
        }

        // python-script 처리결과 json만 가져오기
        const jsonFilePath = stdout.trim().split('\n').slice(-1)[0];  // last line

        fs.readFile(jsonFilePath, 'utf8', (err, data) => {
            if (err) {
                console.error(`Error reading JSON file: ${err}`);
                return res.status(500).json({ error: 'Failed to read segmentation results.' });
            }

            try {
                const result = JSON.parse(data);
                let real_area_display;
                if (result.real_area) {
                    const realAreaValue = parseFloat(result.real_area);

                    switch (unit) {
                        case 'nm':
                            real_area_display = `${realAreaValue.toFixed(2)} nm²`;
                            break;
                        case 'µm':
                            real_area_display = `${realAreaValue.toFixed(2)} µm²`;
                            break;
                        case 'mm':
                            real_area_display = `${realAreaValue.toFixed(2)} mm²`;
                            break;
                        default:
                            real_area_display = `${realAreaValue.toFixed(2)} µm²`;
                            break;
                    }
                }
                // 처리결과 json 형식으로 응답
                res.json({
                    result_img_path: result.result_img_path,
                    analyzed_img_path: result.analyzed_img_path,
                    area_coverage: result.area_coverage,
                    instance_count: result.instance_count,
                    real_area: real_area_display,  // Include the real_area_display in the response
                    message: 'Segmentation completed successfully.'
                });

            } catch (parseError) {
                console.error(`Parse Error: ${parseError.message}`);
                return res.status(500).json({ error: 'Failed to parse result JSON.' });
            }
        });
    });
});

// 예시 이미지 보여주는 기능
app.get('/sample-images', (req, res) => {
    const sampleDir = path.join(__dirname, 'sample');
    fs.readdir(sampleDir, (err, files) => {
        if (err) {
            console.error('Failed to read sample directory:', err);
            return res.status(500).send('Failed to load sample images');
        }
        res.json(files);
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});