# 示例代码架构模板

本文件提供基于"单文件实现"原则的示例代码架构模板。

## 技术约束（默认配置）

1. **服务端默认框架**: 如果用户没有明确指定服务端框架，默认使用 **Next.js**（命令行模式 `create-next-app@latest`）

## 核心设计原则：可读性优先

示例代码的目的是让用户快速理解 SDK 使用方式，而非展示工程化最佳实践。

**原则列表**：

| 原则 | 说明 | 反例（避免） |
|-----|------|-------------|
| 直接调用 | View/Activity 中直接调用 SDK API | 封装成 ZegoEngineManager、ZegoRoomManager |
| 代码集中 | 相关逻辑放在单个文件中 | 分散到多个 Manager/Service 类 |
| 扁平化 | 避免层层嵌套的工具类封装 | Helper 内部再调用其他 Helper |
| 一层到底 | 如果必须有辅助类，方法也应直接调用 SDK | 抽象层、工厂模式等过度设计 |

**唯一允许的封装**：
- 权限相关工具（如 PermissionHelper）
- 配置常量类（从环境变量/配置文件读取）
- UI 组件（如自定义 VideoView）

**配置规范**：
| 配置类型 | 存放位置 | 说明 |
|---------|---------|------|
| AppID、ServerSecret | 环境变量或配置文件 | 与代码分离，不硬编码 |
| Token | 服务端 API 获取 | 客户端不直接生成 |
| RoomID、UserID | 前端页面输入 | 用户根据需要填写 |

## 音视频通话架构模板（Android Java）

### 项目结构

```
VideoCall-Example/
├── app/
│   └── src/
│       └── main/
│           ├── java/com/zego/express/demo/helloworld/
│           │   ├── MainActivity.java           # 主界面（所有逻辑在此文件）
│           │   └── AppConfig.java              # 配置常量（从环境变量读取）
│           ├── res/layout/
│           │   └── activity_main.xml           # 界面布局（含输入框）
│           └── AndroidManifest.xml
├── .env                                     # 环境变量（不提交到 git）
├── .env.example                             # 环境变量示例
├── build.gradle
└── README.md
```

### AppConfig.java（配置类 - 从环境变量读取）

```java
package com.zego.express.demo.helloworld;

public class AppConfig {
    // 从环境变量或 BuildConfig 读取配置，不硬编码
    // AppID / AppID from environment variables or BuildConfig, not hardcoded
    public static final long APP_ID = BuildConfig.APP_ID;

    // Token 服务端地址 / Token server URL
    public static final String TOKEN_SERVER_URL = BuildConfig.TOKEN_SERVER_URL;
}
```

### MainActivity.java（完整示例）

```java

public class MainActivity extends AppCompatActivity {

    // ========== 成员变量 / Member variables ==========
    ZegoExpressEngine engine;
    RequestQueue requestQueue;

    private EditText etRoomId;
    private EditText etUserId;
    private EditText etUserName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 初始化视图 / Initialize views
        etRoomId = findViewById(R.id.etRoomId);
        etUserId = findViewById(R.id.etUserId);
        etUserName = findViewById(R.id.etUserName);

        requestQueue = Volley.newRequestQueue(this);

        // 开始通话按钮 - 直接调用 SDK / Start call button - direct SDK calls
        findViewById(R.id.startButton).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // 获取用户输入 / Get user input
                String roomID = etRoomId.getText().toString();
                String userID = etUserId.getText().toString();
                String userName = etUserName.getText().toString();

                // 验证输入 / Validate input
                if (TextUtils.isEmpty(roomID) || TextUtils.isEmpty(userID)) {
                    Toast.makeText(MainActivity.this, "请填写房间ID和用户ID / Please enter Room ID and User ID", Toast.LENGTH_LONG).show();
                    return;
                }

                createEngine();           // 创建引擎 / Create engine
                setEventHandler();       // 设置回调 / Set event handler
                loginRoomWithToken(roomID, userID, userName);  // 使用 Token 登录房间 / Login room with token
            }
        });

        // 停止通话按钮 / Stop call button
        findViewById(R.id.stopButton).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (engine != null) {
                    engine.logoutRoom();
                    ZegoExpressEngine.destroyEngine(new IZegoDestroyCompletionCallback() {
                        @Override
                        public void onDestroyCompletion() {
                            // 销毁成功 / Destroy completed
                        }
                    });
                    engine = null;
                }
            }
        });
    }

    // ========== 创建引擎（直接调用 SDK）/ Create engine (direct SDK call) ==========
    void createEngine() {
        ZegoEngineProfile profile = new ZegoEngineProfile();
        profile.appID = AppConfig.APP_ID;  // 从配置读取 / Read from config
        profile.scenario = ZegoScenario.DEFAULT;  // 通用场景 / General scenario
        profile.application = getApplication();
        engine = ZegoExpressEngine.createEngine(profile, null);
    }

    // ========== 从服务端获取 Token 并登录房间 / Get token from server and login room ==========
    void loginRoomWithToken(String roomID, String userID, String userName) {
        // 请求服务端生成 Token / Request server to generate token
        String url = AppConfig.TOKEN_SERVER_URL + "/api/token";

        Map<String, String> params = new HashMap<>();
        params.put("roomId", roomID);
        params.put("userId", userID);

        JSONObject jsonObject = new JSONObject(params);

        JsonObjectRequest request = new JsonObjectRequest(
            Request.Method.POST,
            url,
            jsonObject,
            response -> {
                // Token 获取成功 / Token obtained successfully
                String token = response.optString("token");
                if (!TextUtils.isEmpty(token)) {
                    doLoginRoom(roomID, userID, userName, token);
                }
            },
            error -> {
                // Token 获取失败 / Failed to get token
                Toast.makeText(this, "获取 Token 失败 / Failed to get token: " + error.getMessage(), Toast.LENGTH_LONG).show();
            }
        );

        requestQueue.add(request);
    }

    // ========== 执行登录房间操作 / Execute login room ==========
    void doLoginRoom(String roomID, String userID, String userName, String token) {
        ZegoUser user = new ZegoUser(userID, userName);

        ZegoRoomConfig roomConfig = new ZegoRoomConfig();
        roomConfig.token = token;  // 使用 Token 鉴权 / Use token for authentication
        roomConfig.isUserStatusNotify = true;  // 需要接收用户进出回调 / Need user update callback

        // 直接调用登录房间接口 / Direct call to login room
        engine.loginRoom(roomID, user, roomConfig, (int error, JSONObject extendedData) -> {
            if (error == 0) {
                Toast.makeText(this, "登录成功 / Login success", Toast.LENGTH_LONG).show();
                startPublish();  // 开始推流 / Start publishing
            } else {
                Toast.makeText(this, "登录失败 / Login failed: " + error, Toast.LENGTH_LONG).show();
            }
        });
    }

    // ========== 预览并推流（直接调用 SDK）/ Preview and publish (direct SDK call) ==========
    void startPublish() {
        // 设置本地预览视图并启动预览 / Set local preview view and start preview
        ZegoCanvas previewCanvas = new ZegoCanvas(findViewById(R.id.previewView));
        engine.startPreview(previewCanvas);

        // 开始推流 / Start publishing
        // streamID 使用 userID 保证唯一性 / Use userID as streamID for uniqueness
        String streamID = etUserId.getText().toString();
        engine.startPublishingStream(streamID);
    }

    // ========== 设置事件回调（直接在 Activity 内实现）/ Set event handler ==========
    void setEventHandler() {
        engine.setEventHandler(new IZegoEventHandler() {

            // 房间内音视频流增减通知 / Room stream update notification
            @Override
            public void onRoomStreamUpdate(String roomID, ZegoUpdateType updateType,
                    ArrayList<ZegoStream> streamList, JSONObject extendedData) {
                super.onRoomStreamUpdate(roomID, updateType, streamList, extendedData);
                if (updateType == ZegoUpdateType.ADD) {
                    // 有新流，开始拉流 / New stream added, start playing
                    for (ZegoStream stream : streamList) {
                        ZegoCanvas playCanvas = new ZegoCanvas(findViewById(R.id.remoteView));
                        engine.startPlayingStream(stream.streamID, playCanvas);
                    }
                } else if (updateType == ZegoUpdateType.DELETE) {
                    // 流删除，停止拉流 / Stream deleted, stop playing
                    for (ZegoStream stream : streamList) {
                        engine.stopPlayingStream(stream.streamID);
                    }
                }
            }

            // 房间内用户进出通知 / Room user update notification
            @Override
            public void onRoomUserUpdate(String roomID, ZegoUpdateType updateType,
                    ArrayList<ZegoUser> userList) {
                super.onRoomUserUpdate(roomID, updateType, userList);
                if (updateType == ZegoUpdateType.ADD) {
                    for (ZegoUser user : userList) {
                        Toast.makeText(getApplicationContext(),
                            user.userID + " 进入了房间 / joined the room", Toast.LENGTH_LONG).show();
                    }
                } else if (updateType == ZegoUpdateType.DELETE) {
                    for (ZegoUser user : userList) {
                        Toast.makeText(getApplicationContext(),
                            user.userID + " 退出了房间 / left the room", Toast.LENGTH_LONG).show();
                    }
                }
            }

            // 房间连接状态改变 / Room state changed
            @Override
            public void onRoomStateChanged(String roomID, ZegoRoomStateChangedReason reason,
                    int errorCode, JSONObject jsonObject) {
                super.onRoomStateChanged(roomID, reason, errorCode, jsonObject);
                if (reason == ZegoRoomStateChangedReason.LOGINED) {
                    // 登录房间成功 / Login room success
                } else if (reason == ZegoRoomStateChangedReason.LOGIN_FAILED) {
                    // 登录房间失败 / Login room failed
                    Toast.makeText(MainActivity.this,
                        "登录失败 / Login failed: " + errorCode, Toast.LENGTH_LONG).show();
                }
            }

            // 推流状态通知 / Publisher state update
            @Override
            public void onPublisherStateUpdate(String streamID, ZegoPublisherState state,
                    int errorCode, JSONObject extendedData) {
                super.onPublisherStateUpdate(streamID, state, errorCode, extendedData);
                if (state == ZegoPublisherState.PUBLISHING) {
                    // 正在推流中 / Publishing
                } else if (state == ZegoPublisherState.NO_PUBLISH) {
                    // 未推流 / No publishing
                }
            }

            // 拉流状态通知 / Player state update
            @Override
            public void onPlayerStateUpdate(String streamID, ZegoPlayerState state,
                    int errorCode, JSONObject extendedData) {
                super.onPlayerStateUpdate(streamID, state, errorCode, extendedData);
                if (state == ZegoPlayerState.PLAYING) {
                    // 正在拉流中 / Playing
                } else if (state == ZegoPlayerState.NO_PLAY) {
                    // 未拉流 / No playing
                }
            }
        });
    }
}
```

### .env.example（环境变量示例）

```bash
# AppID / AppID
APP_ID=1234567890

# Token 服务端地址 / Token server URL
TOKEN_SERVER_URL=https://your-server.com
```

### 关键点说明

1. **所有 SDK 调用都在 MainActivity 内完成** / All SDK calls are in MainActivity
2. **回调通过匿名内部类直接实现** / Callbacks implemented via anonymous inner class
3. **AppID 从环境变量读取，不硬编码** / AppID from environment, not hardcoded
4. **RoomID、UserID 通过页面输入获取** / RoomID and UserID from page input
5. **Token 从服务端 API 获取** / Token obtained from server API

## 音视频通话架构模板（Web - React）

### 项目结构

```
Web-Example/
├── src/
│   ├── App.tsx                        # 主应用组件
│   ├── index.tsx                      # 入口文件
│   ├── config.ts                      # 配置文件（从环境变量读取）
│   └── styles.css                     # 样式文件
├── .env                               # 环境变量
├── .env.example                       # 环境变量示例
├── package.json
├── tsconfig.json
└── README.md
```

### config.ts（配置文件）

```typescript
// 配置从环境变量读取 / Config from environment variables
export const config = {
  // AppID / AppID
  APP_ID: Number(import.meta.env.VITE_APP_ID) || 0,

  // Token 服务端地址 / Token server URL
  TOKEN_SERVER_URL: import.meta.env.VITE_TOKEN_SERVER_URL || '',
};
```

### App.tsx（完整示例）

```tsx
import { useState, useRef, useEffect } from 'react';
import { ZegoExpressEngine } from 'zego-express-engine-webrtc';
import { config } from './config';
import './styles.css';

function App() {
  // ========== 状态管理 / State management ==========
  const [engine] = useState(() => new ZegoExpressEngine(config.APP_ID, null));
  const [roomId, setRoomId] = useState('room1');
  const [userId, setUserId] = useState('user1');
  const [isJoined, setIsJoined] = useState(false);

  const localVideoRef = useRef<HTMLVideoElement>(null);
  const remoteVideosRef = useRef<Map<string, HTMLVideoElement>>(new Map());

  // ========== 设置回调 / Setup event handlers ==========
  useEffect(() => {
    // 房间状态更新回调 / Room state update callback
    engine.on('roomStateChanged', (roomID, reason, errorCode) => {
      if (reason === 'LOGINED') {
        console.log('登录房间成功 / Login room success');
        setIsJoined(true);
        // 登录成功后开始推流 / Start publishing after login
        startPublishing();
      } else if (reason === 'LOGIN_FAILED') {
        console.error('登录失败 / Login failed:', errorCode);
      }
    });

    // 流更新回调 / Stream update callback
    engine.on('roomStreamUpdate', async (roomID, updateType, streamList) => {
      if (updateType === 'ADD') {
        // 有新流，开始拉流 / New stream added, start playing
        for (const stream of streamList) {
          await startPlayingStream(stream.streamID);
        }
      } else if (updateType === 'DELETE') {
        // 流删除，停止拉流 / Stream deleted, stop playing
        for (const stream of streamList) {
          engine.stopPlayingStream(stream.streamID);
          const videoEl = remoteVideosRef.current.get(stream.streamID);
          if (videoEl) {
            videoEl.remove();
            remoteVideosRef.current.delete(stream.streamID);
          }
        }
      }
    });

    return () => {
      engine.destroyEngine();
    };
  }, [engine]);

  // ========== 从服务端获取 Token / Get token from server ==========
  const getToken = async (roomId: string, userId: string): Promise<string> => {
    const response = await fetch(`${config.TOKEN_SERVER_URL}/api/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ roomId, userId }),
    });

    const data = await response.json();
    return data.token;
  };

  // ========== 登录房间 / Login room ==========
  const loginRoom = async () => {
    const token = await getToken(roomId, userId);

    await engine.loginRoom(roomId, token, { userID: userId, userName: userId }, { userUpdate: true });
  };

  // ========== 开始推流 / Start publishing ==========
  const startPublishing = async () => {
    // 创建本地流 / Create local stream
    const localStream = await engine.createZegoStream();

    // 预览本地流 / Preview local stream
    localStream.playVideo(localVideoRef.current);

    // 开始推流 / Start publishing
    const streamID = userId;
    engine.startPublishingStream(streamID, localStream);
  };

  // ========== 拉取远端流 / Play remote stream ==========
  const startPlayingStream = async (streamID: string) => {
    // 创建视频元素 / Create video element
    const videoEl = document.createElement('video');
    videoEl.autoplay = true;
    videoEl.playsInline = true;
    document.getElementById('remote-container')?.appendChild(videoEl);
    remoteVideosRef.current.set(streamID, videoEl);

    // 开始拉流 / Start playing
    const remoteStream = await engine.startPlayingStream(streamID);
    const remoteView = engine.createRemoteStreamView(remoteStream);
    remoteView.play(videoEl);
  };

  // ========== 退出房间 / Leave room ==========
  const leaveRoom = () => {
    engine.logoutRoom(roomId);
    setIsJoined(false);
  };

  return (
    <div className="app">
      <h1>Zego RTC Video Call / Zego 音视频通话</h1>

      {/* 输入区域 / Input area */}
      <div className="input-section">
        <input
          type="text"
          placeholder="房间 ID / Room ID"
          value={roomId}
          onChange={(e) => setRoomId(e.target.value)}
          disabled={isJoined}
        />
        <input
          type="text"
          placeholder="用户 ID / User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          disabled={isJoined}
        />
        <button onClick={loginRoom} disabled={isJoined}>
          加入房间 / Join Room
        </button>
        <button onClick={leaveRoom} disabled={!isJoined}>
          离开房间 / Leave Room
        </button>
      </div>

      {/* 视频区域 / Video area */}
      <div className="video-section">
        <div className="video-container">
          <h3>本地预览 / Local Preview</h3>
          <video ref={localVideoRef} autoPlay muted playsInline />
        </div>
        <div className="video-container">
          <h3>远端视频 / Remote Video</h3>
          <div id="remote-container" />
        </div>
      </div>
    </div>
  );
}

export default App;
```

### .env.example

```bash
# AppID / AppID
VITE_APP_ID=1234567890

# Token 服务端地址 / Token server URL
VITE_TOKEN_SERVER_URL=https://your-server.com
```

### 关键点说明

1. **使用 React Hooks 管理状态** / Use React Hooks for state management
2. **AppID 从环境变量读取** / AppID from environment variables
3. **RoomID、UserID 通过页面输入** / RoomID and UserID from page input
4. **Token 从服务端 API 获取** / Token obtained from server API
5. **所有逻辑在一个组件文件内** / All logic in single component file

## 服务端架构模板（Node.js + Express）

### 项目结构

```
Server-Example/
├── src/
│   ├── index.js                        # 所有逻辑在此文件
│   └── config.js                      # 配置文件（从环境变量读取）
├── .env                               # 环境变量
├── .env.example                       # 环境变量示例
├── package.json
└── README.md
```

### config.js（配置文件）

```javascript
// 配置从环境变量读取 / Config from environment variables
module.exports = {
  // AppID / AppID
  APP_ID: process.env.APP_ID || 0,

  // ServerSecret / ServerSecret
  SERVER_SECRET: process.env.SERVER_SECRET || '',

  // 端口 / Port
  PORT: process.env.PORT || 3000,
};
```

### index.js（完整示例）

```javascript
const express = require('express');
const cors = require('cors');
const { ZegoServerAssistant } = require('zego-server-assistant');
const { config } = require('./config');

const app = express();
app.use(cors());
app.use(express.json());

// ========== Token 生成接口（直接在路由中实现）/ Token endpoint ==========
app.post('/api/token', (req, res) => {
  const { roomId, userId } = req.body;

  if (!userId) {
    return res.status(400).json({
      error: '缺少参数 / Missing parameter: userId is required'
    });
  }

  // 使用 zego_server_assistant 生成 Token
  // Use zego_server_assistant to generate token
  // 参数：appId, userId, serverSecret, effectiveTimeInSeconds, payload
  // Params: appId, userId, serverSecret, effectiveTimeInSeconds, payload
  const token = ZegoServerAssistant.generateToken04(
    config.APP_ID,
    userId,
    config.SERVER_SECRET,
    3600,                    // Token 有效期 / Token validity period (seconds)
    ''                       // payload：基础鉴权传空字符串 / Empty string for basic auth
  );

  res.json({ token });
});

// ========== 获取房间用户数接口（直接在路由中实现）/ Get room user count ==========
app.get('/api/room/:roomId/users', (req, res) => {
  const { roomId } = req.params;

  // 生成签名参数 / Generate signature parameters
  // 签名算法 / Signature algorithm: md5(AppId + SignatureNonce + ServerSecret + Timestamp)
  const crypto = require('crypto');
  const signatureNonce = crypto.randomBytes(8).toString('hex');
  const timestamp = Math.round(Date.now() / 1000);
  const hash = crypto.createHash('md5');
  hash.update(config.APP_ID + signatureNonce + config.SERVER_SECRET + timestamp);
  const signature = hash.digest('hex');

  // 构建请求 URL / Build request URL
  const params = new URLSearchParams({
    Action: 'DescribeUserNum',
    AppId: config.APP_ID,
    SignatureNonce: signatureNonce,
    Timestamp: timestamp,
    Signature: signature,
    SignatureVersion: '2.0',
    'RoomId[]': roomId
  });

  const url = `https://rtc-api.zego.im/?${params.toString()}`;

  // 发送请求 / Send request
  fetch(url)
    .then(response => response.json())
    .then(data => res.json(data))
    .catch(error => res.status(500).json({ error: error.message }));
});

// ========== 启动服务 / Start server ==========
app.listen(config.PORT, () => {
  console.log(`服务运行在端口 / Server running on port ${config.PORT}`);
});
```

### .env.example

```bash
# AppID / AppID
APP_ID=1234567890

# ServerSecret / ServerSecret（请妥善保管 / Keep it secret）
SERVER_SECRET=your_server_secret_here

# 端口 / Port
PORT=3000
```

### 关键点说明

1. **所有逻辑在 index.js 一个文件内** / All logic in single index.js file
2. **AppID、ServerSecret 从环境变量读取** / AppID and ServerSecret from environment
3. **Token 生成使用 `zego-server-assistant` 插件** / Use zego-server-assistant for token generation
4. **服务端 API 调用使用 MD5 签名** / Server API calls use MD5 signature
5. **业务逻辑直接在路由处理函数中实现** / Business logic directly in route handlers

## 快捷参考：各平台标准入口

| 平台 | 核心文件 | SDK 初始化位置 | 配置来源 |
|-----|---------|---------------|---------|
| Android Java | MainActivity.java | createEngine() 方法 | BuildConfig / .env |
| iOS Swift | ViewController.swift | viewDidLoad() 方法 | Config.xcconfig |
| Web (React) | App.tsx | useState() 初始化 | .env |
| Node.js | index.js | app.listen() 之前 | .env |

## 反模式：不要这样写

### ❌ 错误示例：层层封装

```java
// 不要这样做：Manager 套 Manager
// Don't do this: Manager wrapping Manager
MainActivity
    └── ZegoEngineManager
            └── ZegoRoomManager
                    └── ZegoStreamManager
                            └── ZegoEventHandler
```

用户需要打开 5 个文件才能理解登录房间的逻辑 / Users need to open 5 files to understand login room logic.

### ❌ 错误示例：硬编码配置

```java
// 不要这样做：配置硬编码
// Don't do this: Hardcoded config
long appId = 1234567890;  // 硬编码 / Hardcoded
String roomID = "room1";  // 硬编码 / Hardcoded
```

### ✅ 正确示例：单文件 + 配置分离

```java
// 应该这样：所有逻辑在一个 Activity 内，配置从环境变量读取
// Should do: All logic in one Activity, config from environment
MainActivity
    ├── createEngine(): 直接 ZegoExpressEngine.createEngine(profile)
    │   └── profile.appID = BuildConfig.APP_ID  // 从配置读取
    ├── loginRoom(): 直接 engine.loginRoom()
    │   └── roomID = etRoomId.getText()  // 用户输入
    ├── setEventHandler(): 直接实现 IZegoEventHandler
    └── getToken(): 从服务端获取 Token
```

用户阅读一个文件就能理解完整流程 / Users can understand the complete flow in one file.
