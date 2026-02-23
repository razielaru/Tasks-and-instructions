<!DOCTYPE html>
<html lang="he" dir="rtl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>מערך הרבנות - פקודות ומשימות</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Heebo', 'sans-serif'] },
                    colors: {
                        idf: { light: '#7B8A62', DEFAULT: '#4E5A37', dark: '#2E3521' },
                        gold: { DEFAULT: '#D4AF37', light: '#F3E5AB' }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #f1f5f0;
            background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239ca3af' fill-opacity='0.08'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        }

        /* Checkbox */
        .task-checkbox {
            appearance: none;
            background-color: #fff;
            width: 1.4em;
            height: 1.4em;
            border: 2px solid #cbd5e1;
            border-radius: 0.3em;
            display: grid;
            place-content: center;
            cursor: pointer;
            transition: all 0.2s;
            flex-shrink: 0;
            margin-top: 3px;
        }

        .task-checkbox::before {
            content: "";
            width: 0.75em;
            height: 0.75em;
            clip-path: polygon(14% 44%, 0 65%, 50% 100%, 100% 16%, 80% 0%, 43% 62%);
            transform: scale(0);
            background-color: white;
            transition: 120ms transform ease-in-out;
        }

        .task-checkbox:checked {
            background-color: #4E5A37;
            border-color: #4E5A37;
        }

        .task-checkbox:checked::before {
            transform: scale(1);
        }

        .task-row:has(.task-checkbox:checked) .task-title {
            color: #9ca3af;
            text-decoration: line-through;
        }

        .task-row:has(.task-checkbox:checked) .task-desc {
            color: #d1d5db;
        }

        .task-row:has(.task-checkbox:checked) {
            opacity: 0.75;
            background-color: #f8fafc;
        }

        /* Tabs */
        .tab-btn {
            transition: all 0.2s;
            border-bottom: 3px solid transparent;
        }

        .tab-btn.active {
            border-bottom-color: #4E5A37;
            color: #4E5A37;
            font-weight: 800;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Progress ring */
        .progress-ring-circle {
            transition: stroke-dashoffset 0.5s ease;
            transform: rotate(-90deg);
            transform-origin: 50% 50%;
        }

        @media print {
            .no-print {
                display: none !important;
            }

            body {
                background: white;
            }
        }
    </style>
</head>

<body class="text-gray-800 antialiased pb-16 font-sans">

    <!-- ======================== LOGIN SCREEN ======================== -->
    <div id="loginScreen" class="min-h-screen flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl shadow-xl p-8 md:p-12 w-full max-w-md text-center">
            <div class="bg-idf rounded-2xl p-6 mb-6 text-white">
                <i class="ph-fill ph-star-of-david text-5xl text-gold block mb-2"></i>
                <h1 class="text-2xl font-extrabold">מערך הרבנות</h1>
                <p class="text-gray-300 text-sm mt-1">פקודות ומשימות - פורים ופסח</p>
            </div>
            <h2 class="text-xl font-bold text-gray-700 mb-6">מי אתה?</h2>
            <div class="grid grid-cols-2 gap-3 mb-6">
                <button onclick="login('רב האוגדה')"
                    class="login-btn col-span-2 bg-gold text-idf-dark font-bold py-3 px-4 rounded-xl hover:opacity-90 transition flex items-center justify-center gap-2 text-lg">
                    <i class="ph-fill ph-crown"></i> רב האוגדה
                </button>
                <button onclick="login('בנימין')"
                    class="login-btn bg-idf text-white font-bold py-3 px-4 rounded-xl hover:bg-idf-light transition">חטמ"ר
                    בנימין</button>
                <button onclick="login('שומרון')"
                    class="login-btn bg-idf text-white font-bold py-3 px-4 rounded-xl hover:bg-idf-light transition">חטמ"ר
                    שומרון</button>
                <button onclick="login('אפרים')"
                    class="login-btn bg-idf text-white font-bold py-3 px-4 rounded-xl hover:bg-idf-light transition">חטמ"ר
                    אפרים</button>
                <button onclick="login('מנשה')"
                    class="login-btn bg-idf text-white font-bold py-3 px-4 rounded-xl hover:bg-idf-light transition">חטמ"ר
                    מנשה</button>
                <button onclick="login('יהודה')"
                    class="login-btn bg-idf text-white font-bold py-3 px-4 rounded-xl hover:bg-idf-light transition">חטמ"ר
                    יהודה</button>
                <button onclick="login('עציון')"
                    class="login-btn bg-idf text-white font-bold py-3 px-4 rounded-xl hover:bg-idf-light transition">חטמ"ר
                    עציון</button>
            </div>
            <p class="text-xs text-gray-400">הבחירה נשמרת בדפדפן שלך</p>
        </div>
    </div>

    <!-- ======================== MAIN APP ======================== -->
    <div id="mainApp" class="hidden">

        <!-- Header -->
        <header class="bg-idf text-white shadow-lg sticky top-0 z-50">
            <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <i class="ph-fill ph-star-of-david text-3xl text-gold"></i>
                    <div>
                        <h1 class="text-lg md:text-xl font-extrabold leading-tight">מערך הרבנות - פקודות ומשימות</h1>
                        <p class="text-xs text-gray-300">מחובר בתור: <span id="userLabel"
                                class="text-gold font-bold"></span></p>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="exportToExcel()"
                        class="no-print hidden md:flex items-center gap-1 bg-green-700 text-white text-sm px-3 py-1.5 rounded-lg hover:bg-green-800 transition font-bold">
                        <i class="ph ph-microsoft-excel-logo"></i> אקסל
                    </button>
                    <button onclick="logout()"
                        class="no-print flex items-center gap-1 bg-white/20 text-white text-sm px-3 py-1.5 rounded-lg hover:bg-white/30 transition font-bold">
                        <i class="ph ph-sign-out"></i> <span class="hidden md:inline">החלף משתמש</span>
                    </button>
                </div>
            </div>
            <!-- Tabs (only shown for רב האוגדה) -->
            <div id="tabBar" class="hidden bg-idf-dark overflow-x-auto">
                <div class="max-w-5xl mx-auto px-4 flex gap-1 min-w-max">
                    <button class="tab-btn active text-white text-sm py-2.5 px-4 whitespace-nowrap"
                        onclick="switchTab('כולם')">🌐 סקירה כללית</button>
                    <button class="tab-btn text-gray-300 text-sm py-2.5 px-4 whitespace-nowrap"
                        onclick="switchTab('בנימין')">בנימין</button>
                    <button class="tab-btn text-gray-300 text-sm py-2.5 px-4 whitespace-nowrap"
                        onclick="switchTab('שומרון')">שומרון</button>
                    <button class="tab-btn text-gray-300 text-sm py-2.5 px-4 whitespace-nowrap"
                        onclick="switchTab('אפרים')">אפרים</button>
                    <button class="tab-btn text-gray-300 text-sm py-2.5 px-4 whitespace-nowrap"
                        onclick="switchTab('מנשה')">מנשה</button>
                    <button class="tab-btn text-gray-300 text-sm py-2.5 px-4 whitespace-nowrap"
                        onclick="switchTab('יהודה')">יהודה</button>
                    <button class="tab-btn text-gray-300 text-sm py-2.5 px-4 whitespace-nowrap"
                        onclick="switchTab('עציון')">עציון</button>
                </div>
            </div>
            <!-- Progress bar for brigade rabbi -->
            <div id="progressBarWrap" class="bg-idf-dark h-1.5 w-full">
                <div id="progressBar" class="bg-gold h-full transition-all duration-500" style="width:0%"></div>
            </div>
        </header>

        <main class="max-w-5xl mx-auto px-4 mt-6 space-y-6">

            <!-- ===== BRIGADE RABBI VIEW ===== -->
            <div id="brigadeView" class="hidden space-y-6">
                <!-- Stats row -->
                <div class="grid grid-cols-3 gap-3">
                    <div class="bg-white rounded-xl shadow-sm p-4 text-center border-t-4 border-idf">
                        <p class="text-3xl font-extrabold text-idf" id="statTotal">0</p>
                        <p class="text-xs text-gray-500 mt-1">סה"כ משימות</p>
                    </div>
                    <div class="bg-white rounded-xl shadow-sm p-4 text-center border-t-4 border-green-500">
                        <p class="text-3xl font-extrabold text-green-600" id="statDone">0</p>
                        <p class="text-xs text-gray-500 mt-1">הושלמו</p>
                    </div>
                    <div class="bg-white rounded-xl shadow-sm p-4 text-center border-t-4 border-orange-400">
                        <p class="text-3xl font-extrabold text-orange-500" id="statLeft">0</p>
                        <p class="text-xs text-gray-500 mt-1">נותרו</p>
                    </div>
                </div>

                <!-- Global tasks (from division rabbi) -->
                <section>
                    <div class="flex items-center gap-2 mb-3">
                        <div class="bg-gold/30 p-2 rounded-lg"><i class="ph-fill ph-broadcast text-idf text-xl"></i>
                        </div>
                        <h2 class="text-xl font-bold text-gray-800">משימות אוגדתיות</h2>
                        <span class="text-xs bg-idf text-white px-2 py-0.5 rounded-full">מרב האוגדה</span>
                    </div>
                    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                        <ul id="globalTaskList" class="divide-y divide-gray-100"></ul>
                        <div id="globalEmpty" class="hidden p-6 text-center text-gray-400 text-sm">אין עדיין משימות
                            אוגדתיות</div>
                    </div>
                </section>

                <!-- Local tasks -->
                <section>
                    <div class="flex items-center justify-between gap-2 mb-3">
                        <div class="flex items-center gap-2">
                            <div class="bg-idf p-2 rounded-lg text-white"><i class="ph-fill ph-list-checks text-xl"></i>
                            </div>
                            <h2 class="text-xl font-bold text-gray-800">המשימות שלי</h2>
                        </div>
                        <button onclick="openAddTaskModal('local')"
                            class="no-print flex items-center gap-1 bg-idf text-white text-sm px-4 py-2 rounded-full hover:bg-idf-light transition font-bold">
                            <i class="ph ph-plus"></i> הוסף משימה
                        </button>
                    </div>
                    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                        <ul id="localTaskList" class="divide-y divide-gray-100"></ul>
                        <div id="localEmpty" class="p-6 text-center text-gray-400 text-sm">
                            <i class="ph ph-clipboard-text text-3xl block mb-2"></i>
                            לחץ "+ הוסף משימה" כדי להוסיף משימה
                        </div>
                    </div>
                </section>

                <!-- Schedule section -->
                <section>
                    <div class="flex items-center gap-2 mb-3">
                        <div class="bg-idf-light p-2 rounded-lg text-white"><i class="ph-fill ph-calendar text-xl"></i>
                        </div>
                        <h2 class="text-xl font-bold text-gray-800">לו"ז שבועי: כנסים וישיבות</h2>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="bg-white rounded-xl shadow-sm p-5 border-t-4 border-idf">
                            <div class="flex justify-between items-start mb-2">
                                <span class="bg-gray-100 text-gray-800 text-sm font-bold px-3 py-1 rounded-full">יום
                                    שני</span>
                                <i class="ph-fill ph-users-three text-idf-light text-xl"></i>
                            </div>
                            <h3 class="text-lg font-bold mb-2">כנס פסח פיקודי</h3>
                            <p class="text-sm text-gray-600 mb-3"><strong>נוכחות:</strong> רבנים, נגדים וחיילי רבנות
                                בחזית.</p>
                            <div
                                class="bg-yellow-50 text-yellow-800 text-sm p-3 rounded-lg border border-yellow-200 flex items-start gap-2">
                                <i class="ph-fill ph-warning-circle mt-0.5 flex-shrink-0"></i>
                                <span><strong>דגש:</strong> להשאיר כוח אדם בגזרה למתן מענה לכשרות.</span>
                            </div>
                        </div>
                        <div class="bg-white rounded-xl shadow-sm p-5 border-t-4 border-idf">
                            <div class="flex justify-between items-start mb-2">
                                <span class="bg-gray-100 text-gray-800 text-sm font-bold px-3 py-1 rounded-full">יום
                                    רביעי</span>
                                <i class="ph-fill ph-chalkboard-teacher text-idf-light text-xl"></i>
                            </div>
                            <h3 class="text-lg font-bold mb-2">יום ישיבה אוגדתי</h3>
                            <p class="text-sm text-gray-600 mb-3"><strong>נוכחות:</strong> כלל רבני, נגדי וחיילי אוגדת
                                איו"ש.</p>
                            <div
                                class="bg-red-50 text-red-800 text-sm p-3 rounded-lg border border-red-200 flex items-start gap-2">
                                <i class="ph-fill ph-prohibit mt-0.5 flex-shrink-0"></i>
                                <span><strong>דגש:</strong> נוכחות חובה. אין שחרורים לאף אחד!</span>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Mobile export -->
                <div class="no-print flex justify-center gap-3 md:hidden">
                    <button onclick="exportToExcel()"
                        class="flex items-center gap-2 bg-green-700 text-white px-5 py-2.5 rounded-full font-bold shadow hover:bg-green-800 transition text-sm">
                        <i class="ph ph-microsoft-excel-logo"></i> ייצוא לאקסל
                    </button>
                </div>
            </div>

            <!-- ===== DIVISION RABBI VIEW ===== -->
            <div id="divisionView" class="hidden">

                <!-- Tab: Overview -->
                <div id="tab-כולם" class="tab-content active space-y-6">
                    <div class="bg-white rounded-2xl shadow-sm p-6 border-r-4 border-gold">
                        <h2 class="text-xl font-bold mb-4 flex items-center gap-2"><i
                                class="ph-fill ph-chart-bar text-idf text-2xl"></i> סקירה כללית - כל החטמ"רים</h2>
                        <div id="overviewGrid" class="grid grid-cols-2 md:grid-cols-3 gap-4"></div>
                    </div>
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <h2 class="text-xl font-bold flex items-center gap-2"><i
                                    class="ph-fill ph-broadcast text-gold text-2xl"></i> משימות אוגדתיות (לכולם)</h2>
                            <button onclick="openAddTaskModal('global')"
                                class="no-print flex items-center gap-1 bg-gold text-idf-dark text-sm px-4 py-2 rounded-full hover:opacity-90 transition font-bold">
                                <i class="ph ph-plus"></i> הוסף לכולם
                            </button>
                        </div>
                        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                            <ul id="globalTaskListAdmin" class="divide-y divide-gray-100"></ul>
                            <div id="globalEmptyAdmin" class="hidden p-6 text-center text-gray-400 text-sm">אין עדיין
                                משימות אוגדתיות</div>
                        </div>
                    </div>
                </div>

                <!-- Per-Brigade Tabs -->
                <div id="tab-בנימין" class="tab-content hidden"></div>
                <div id="tab-שומרון" class="tab-content hidden"></div>
                <div id="tab-אפרים" class="tab-content hidden"></div>
                <div id="tab-מנשה" class="tab-content hidden"></div>
                <div id="tab-יהודה" class="tab-content hidden"></div>
                <div id="tab-עציון" class="tab-content hidden"></div>
            </div>

        </main>
    </div>

    <!-- ======================== ADD TASK MODAL ======================== -->
    <div id="addTaskModal" class="hidden fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md">
            <h3 id="modalTitle" class="text-xl font-bold mb-4 text-gray-800">הוספת משימה</h3>
            <div class="space-y-3">
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">כותרת המשימה *</label>
                    <input id="taskTitleInput" type="text"
                        class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-idf"
                        placeholder="כותרת קצרה וברורה">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">פירוט</label>
                    <textarea id="taskDescInput" rows="3"
                        class="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-idf resize-none"
                        placeholder="הוסף הוראות, הבהרות..."></textarea>
                </div>
                <label class="flex items-center gap-2 cursor-pointer text-sm">
                    <input type="checkbox" id="taskUrgentInput" class="w-4 h-4 accent-red-600">
                    <span class="font-medium text-red-600">סמן כ"חובת עדכון"</span>
                </label>
            </div>
            <div class="flex gap-3 mt-5">
                <button onclick="submitTask()"
                    class="flex-1 bg-idf text-white font-bold py-2.5 rounded-xl hover:bg-idf-light transition">הוסף
                    משימה</button>
                <button onclick="closeModal()"
                    class="flex-1 bg-gray-100 text-gray-700 font-bold py-2.5 rounded-xl hover:bg-gray-200 transition">ביטול</button>
            </div>
        </div>
    </div>

    <script>
        // ─── CONSTANTS ───────────────────────────────────────────────
        const BRIGADES = ['בנימין', 'שומרון', 'אפרים', 'מנשה', 'יהודה', 'עציון'];
        const STORAGE_KEY = 'rabbinate_v2';

        // ─── DEFAULT TASKS ────────────────────────────────────────────
        const DEFAULT_GLOBAL_TASKS = [
            { id: 'g1', title: 'היערכות לציוד קריאה בבתי הכנסת', desc: 'יש לבדוק שיש מגילת אסתר מקלף בכל בית כנסת ומגילות מנייר. שימו את מגילת הקלף בארון הקודש והודיעו לחיילים להוציאה רק בפורים.', urgent: false, category: 'פורים' },
            { id: 'g2', title: 'קוראי מגילה במוצבים', desc: 'לוודא ולעדכן שבכל מוצב פלוגתי יש קורא מגילה (שם + טלפון). לוודא חבירה לחב"ד המרחבי לדאוג לקריאות בפילבוקסים ובסיורים.', urgent: true, category: 'פורים' },
            { id: 'g3', title: 'פרסום לו"ז פורים בבסיסים', desc: 'לפרסם לו"ז לתענית אסתר וקריאות מגילה: ערב (צאת הצום ולאחריו בחמ"ל), ובוקר (שחרית ולאחר שחרית).', urgent: false, category: 'פורים' },
            { id: 'g4', title: 'הנחיות הלכה למעשה', desc: 'לפרסם הנחיות חטיבתיות על פי "הלכה כסדרה" - איך עושים משלוח מנות ומתנות לאביונים.', urgent: false, category: 'פורים' },
            { id: 'g5', title: 'תיאום סעודות החג', desc: 'לתאם מול רס"ר מטבח: סעודה מפסקת (פתיחת צום), שבירת הצום, וסעודת החג.', urgent: false, category: 'פורים' },
            { id: 'g6', title: 'כשרות תרומות', desc: 'לוודא מול רס"ר המחנה את תרומות משלוחי המנות המגיעות לחיילים - שהכל כשר ללא ספק.', urgent: false, category: 'פורים' },
            { id: 'g7', title: 'קפ"ק חטיבתי מורחב', desc: 'לוודא ולעדכן שנקבע קפ"ק בראשות סמח"ט, קל"ח, רס"ר ונציגים רלוונטיים (מנהל מטבח).', urgent: true, category: 'פסח' },
            { id: 'g8', title: 'קפ"קים גדודיים', desc: 'לוודא קיום קפ"קים בכל הגדודים (מג"ד, סמג"ד, מ"פים) בתיאום עם רב החטיבה. המטרה: היכשרות, ניקיונות והשבתות.', urgent: false, category: 'פסח' },
            { id: 'g9', title: 'זימון אנשי מילואים', desc: 'לוודא שלכל "אנשי הפסח" יצא צו מילואים מסודר. דגש על חיילים שבפטור ובסיפוח.', urgent: false, category: 'פסח' },
            { id: 'g10', title: 'איתור כוח אדם נוסף', desc: 'להמשיך לחפש ולאתר אנשי מילואים נוספים לטובת מאמץ ההכשרות במחנות ובמוצבים.', urgent: false, category: 'פסח' },
        ];

        // ─── STATE ────────────────────────────────────────────────────
        let currentUser = null;
        let currentTab = 'כולם';
        let modalMode = null; // 'global' | 'local' | brigade name
        let data = {};

        // ─── STORAGE ─────────────────────────────────────────────────
        function loadData() {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (raw) {
                data = JSON.parse(raw);
            } else {
                data = {
                    globalTasks: [...DEFAULT_GLOBAL_TASKS],
                    brigadeTasks: {},
                    completions: {}
                };
                BRIGADES.forEach(b => {
                    data.brigadeTasks[b] = [];
                    data.completions[b] = {};
                });
                saveData();
            }
        }
        function saveData() {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        }

        // ─── LOGIN ───────────────────────────────────────────────────
        function login(user) {
            currentUser = user;
            localStorage.setItem('currentUser', user);
            document.getElementById('loginScreen').classList.add('hidden');
            document.getElementById('mainApp').classList.remove('hidden');
            document.getElementById('userLabel').textContent = user === 'רב האוגדה' ? 'רב האוגדה' : 'חטמ"ר ' + user;
            if (user === 'רב האוגדה') {
                document.getElementById('tabBar').classList.remove('hidden');
                document.getElementById('divisionView').classList.remove('hidden');
                document.getElementById('progressBarWrap').classList.add('hidden');
                renderDivisionView();
            } else {
                document.getElementById('brigadeView').classList.remove('hidden');
                document.getElementById('progressBarWrap').classList.remove('hidden');
                renderBrigadeView(user);
            }
        }
        function logout() {
            localStorage.removeItem('currentUser');
            location.reload();
        }

        // ─── RENDER: BRIGADE ─────────────────────────────────────────
        function renderBrigadeView(brigade) {
            renderGlobalTaskList('globalTaskList', 'globalEmpty', brigade);
            renderLocalTaskList(brigade);
            updateStats(brigade);
        }

        function renderGlobalTaskList(listId, emptyId, brigade) {
            const ul = document.getElementById(listId);
            const empty = document.getElementById(emptyId);
            ul.innerHTML = '';
            if (!data.globalTasks || data.globalTasks.length === 0) {
                empty.classList.remove('hidden'); return;
            }
            empty.classList.add('hidden');
            data.globalTasks.forEach(task => {
                const checked = data.completions[brigade] && data.completions[brigade]['g_' + task.id];
                ul.appendChild(createTaskItem(task, checked, (val) => {
                    if (!data.completions[brigade]) data.completions[brigade] = {};
                    data.completions[brigade]['g_' + task.id] = val;
                    saveData();
                    updateStats(brigade);
                }, false));
            });
        }

        function renderLocalTaskList(brigade) {
            const ul = document.getElementById('localTaskList');
            const empty = document.getElementById('localEmpty');
            ul.innerHTML = '';
            const tasks = data.brigadeTasks[brigade] || [];
            if (tasks.length === 0) { empty.classList.remove('hidden'); return; }
            empty.classList.add('hidden');
            tasks.forEach(task => {
                const checked = data.completions[brigade] && data.completions[brigade]['l_' + task.id];
                ul.appendChild(createTaskItem(task, checked, (val) => {
                    if (!data.completions[brigade]) data.completions[brigade] = {};
                    data.completions[brigade]['l_' + task.id] = val;
                    saveData();
                    updateStats(brigade);
                }, true, () => deleteLocalTask(brigade, task.id)));
            });
        }

        function createTaskItem(task, checked, onChange, canDelete, onDelete) {
            const li = document.createElement('li');
            li.className = 'task-row p-4 hover:bg-gray-50 transition flex gap-3 items-start';
            const checkId = 'cb_' + Math.random().toString(36).substr(2, 8);
            li.innerHTML = `
        <input type="checkbox" id="${checkId}" class="task-checkbox" ${checked ? 'checked' : ''}>
        <label for="${checkId}" class="flex-1 cursor-pointer">
            <span class="task-title flex items-center gap-2 font-bold text-gray-800 mb-0.5">
                ${task.title}
                ${task.urgent ? '<span class="bg-red-100 text-red-700 text-xs px-2 py-0.5 rounded-full font-bold shrink-0">חובת עדכון</span>' : ''}
                ${task.category ? '<span class="bg-idf/10 text-idf text-xs px-2 py-0.5 rounded-full shrink-0">' + task.category + '</span>' : ''}
            </span>
            ${task.desc ? '<span class="task-desc block text-sm text-gray-500">' + task.desc + '</span>' : ''}
        </label>
        ${canDelete ? '<button class="no-print text-gray-300 hover:text-red-400 transition shrink-0 mt-0.5" onclick="this.closest(\'li\').remove(); onDelete && onDelete()"><i class="ph ph-trash text-lg"></i></button>' : ''}
    `;
            li.querySelector('input').addEventListener('change', (e) => onChange(e.target.checked));
            if (canDelete && onDelete) {
                li.querySelector('button')?.addEventListener('click', onDelete);
            }
            return li;
        }

        function updateStats(brigade) {
            const globalCount = data.globalTasks.length;
            const localCount = (data.brigadeTasks[brigade] || []).length;
            const total = globalCount + localCount;
            const comp = data.completions[brigade] || {};
            const done = Object.values(comp).filter(Boolean).length;
            document.getElementById('statTotal').textContent = total;
            document.getElementById('statDone').textContent = done;
            document.getElementById('statLeft').textContent = Math.max(0, total - done);
            const pct = total === 0 ? 0 : Math.round((done / total) * 100);
            document.getElementById('progressBar').style.width = pct + '%';
        }

        function deleteLocalTask(brigade, taskId) {
            data.brigadeTasks[brigade] = (data.brigadeTasks[brigade] || []).filter(t => t.id !== taskId);
            delete (data.completions[brigade] || {})['l_' + taskId];
            saveData();
            renderLocalTaskList(brigade);
            updateStats(brigade);
        }

        // ─── RENDER: DIVISION ─────────────────────────────────────────
        function renderDivisionView() {
            renderGlobalTaskListAdmin();
            renderOverviewGrid();
            BRIGADES.forEach(b => renderBrigadeTabForAdmin(b));
        }

        function renderGlobalTaskListAdmin() {
            const ul = document.getElementById('globalTaskListAdmin');
            const empty = document.getElementById('globalEmptyAdmin');
            ul.innerHTML = '';
            if (!data.globalTasks || data.globalTasks.length === 0) {
                empty.classList.remove('hidden'); return;
            }
            empty.classList.add('hidden');
            data.globalTasks.forEach(task => {
                const li = document.createElement('li');
                li.className = 'p-4 flex gap-3 items-start hover:bg-gray-50';
                li.innerHTML = `
            <div class="flex-1">
                <span class="flex items-center gap-2 font-bold text-gray-800 mb-0.5">
                    ${task.title}
                    ${task.urgent ? '<span class="bg-red-100 text-red-700 text-xs px-2 py-0.5 rounded-full font-bold">חובת עדכון</span>' : ''}
                    ${task.category ? '<span class="bg-idf/10 text-idf text-xs px-2 py-0.5 rounded-full">' + task.category + '</span>' : ''}
                </span>
                ${task.desc ? '<span class="block text-sm text-gray-500">' + task.desc + '</span>' : ''}
            </div>
            <button class="no-print text-gray-300 hover:text-red-400 transition shrink-0" onclick="deleteGlobalTask('${task.id}')"><i class="ph ph-trash text-lg"></i></button>
        `;
                ul.appendChild(li);
            });
        }

        function renderOverviewGrid() {
            const grid = document.getElementById('overviewGrid');
            grid.innerHTML = '';
            BRIGADES.forEach(b => {
                const total = data.globalTasks.length + (data.brigadeTasks[b] || []).length;
                const comp = data.completions[b] || {};
                const done = Object.values(comp).filter(Boolean).length;
                const pct = total === 0 ? 0 : Math.round((done / total) * 100);
                const color = pct === 100 ? 'border-green-500 bg-green-50' : pct >= 50 ? 'border-yellow-400 bg-yellow-50' : 'border-red-300 bg-red-50';
                const textColor = pct === 100 ? 'text-green-600' : pct >= 50 ? 'text-yellow-600' : 'text-red-500';
                grid.innerHTML += `
            <div class="border-2 ${color} rounded-xl p-4 cursor-pointer hover:shadow-md transition" onclick="switchTab('${b}')">
                <p class="font-bold text-gray-700 mb-2">${b}</p>
                <p class="text-3xl font-extrabold ${textColor}">${pct}%</p>
                <p class="text-xs text-gray-500 mt-1">${done} / ${total} משימות</p>
                <div class="bg-gray-200 rounded-full h-1.5 mt-2">
                    <div class="bg-idf h-1.5 rounded-full" style="width:${pct}%"></div>
                </div>
            </div>`;
            });
        }

        function renderBrigadeTabForAdmin(brigade) {
            const container = document.getElementById('tab-' + brigade);
            container.innerHTML = '';
            const globalCount = data.globalTasks.length;
            const localTasks = data.brigadeTasks[brigade] || [];
            const total = globalCount + localTasks.length;
            const comp = data.completions[brigade] || {};
            const done = Object.values(comp).filter(Boolean).length;
            const pct = total === 0 ? 0 : Math.round((done / total) * 100);

            container.innerHTML = `
        <div class="space-y-5">
            <div class="bg-white rounded-2xl shadow-sm p-5 flex items-center gap-4">
                <div class="text-center">
                    <p class="text-4xl font-extrabold text-idf">${pct}%</p>
                    <p class="text-xs text-gray-500">הושלם</p>
                </div>
                <div class="flex-1">
                    <div class="bg-gray-200 rounded-full h-3">
                        <div class="bg-idf h-3 rounded-full transition-all" style="width:${pct}%"></div>
                    </div>
                    <p class="text-sm text-gray-500 mt-1">${done} מתוך ${total} משימות הושלמו</p>
                </div>
            </div>

            <div>
                <div class="flex items-center justify-between mb-3">
                    <h3 class="font-bold text-gray-700 flex items-center gap-2"><i class="ph-fill ph-broadcast text-gold"></i> משימות אוגדתיות</h3>
                </div>
                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                    <ul class="divide-y divide-gray-100">
                        ${data.globalTasks.map(task => {
                const checked = comp['g_' + task.id];
                return `<li class="task-row p-4 flex gap-3 items-start ${checked ? 'opacity-75 bg-gray-50' : ''}">
                                <div class="w-5 h-5 rounded-md border-2 ${checked ? 'bg-idf border-idf' : 'border-gray-300'} flex items-center justify-center shrink-0 mt-0.5">
                                    ${checked ? '<i class="ph-fill ph-check text-white text-xs"></i>' : ''}
                                </div>
                                <div>
                                    <span class="font-bold ${checked ? 'line-through text-gray-400' : 'text-gray-800'}">${task.title}</span>
                                    ${task.urgent ? '<span class="mr-2 bg-red-100 text-red-700 text-xs px-1.5 py-0.5 rounded-full">חובת עדכון</span>' : ''}
                                </div>
                            </li>`;
            }).join('')}
                    </ul>
                </div>
            </div>

            <div>
                <div class="flex items-center justify-between mb-3">
                    <h3 class="font-bold text-gray-700 flex items-center gap-2"><i class="ph-fill ph-list-checks text-idf"></i> משימות חטמ"ר ${brigade}</h3>
                    <button onclick="openAddTaskModal('${brigade}')" class="no-print flex items-center gap-1 bg-idf text-white text-sm px-4 py-2 rounded-full hover:bg-idf-light transition font-bold">
                        <i class="ph ph-plus"></i> הוסף
                    </button>
                </div>
                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                    <ul class="divide-y divide-gray-100" id="adminLocalList_${brigade}">
                        ${localTasks.length === 0 ? '<li class="p-5 text-center text-gray-400 text-sm">אין משימות ספציפיות</li>' : ''}
                        ${localTasks.map(task => {
                const checked = comp['l_' + task.id];
                return `<li class="task-row p-4 flex gap-3 items-start ${checked ? 'opacity-75 bg-gray-50' : ''}">
                                <div class="w-5 h-5 rounded-md border-2 ${checked ? 'bg-idf border-idf' : 'border-gray-300'} flex items-center justify-center shrink-0 mt-0.5">
                                    ${checked ? '<i class="ph-fill ph-check text-white text-xs"></i>' : ''}
                                </div>
                                <div class="flex-1">
                                    <span class="font-bold ${checked ? 'line-through text-gray-400' : 'text-gray-800'}">${task.title}</span>
                                    ${task.urgent ? '<span class="mr-2 bg-red-100 text-red-700 text-xs px-1.5 py-0.5 rounded-full">חובת עדכון</span>' : ''}
                                    ${task.desc ? '<span class="block text-sm text-gray-500">' + task.desc + '</span>' : ''}
                                </div>
                                <button class="no-print text-gray-300 hover:text-red-400" onclick="deleteLocalTaskFromAdmin('${brigade}', '${task.id}')"><i class="ph ph-trash text-lg"></i></button>
                            </li>`;
            }).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
        }

        function deleteGlobalTask(taskId) {
            if (!confirm('האם למחוק משימה זו מכל החטמ"רים?')) return;
            data.globalTasks = data.globalTasks.filter(t => t.id !== taskId);
            saveData();
            renderDivisionView();
        }

        function deleteLocalTaskFromAdmin(brigade, taskId) {
            data.brigadeTasks[brigade] = (data.brigadeTasks[brigade] || []).filter(t => t.id !== taskId);
            delete (data.completions[brigade] || {})['l_' + taskId];
            saveData();
            renderBrigadeTabForAdmin(brigade);
            renderOverviewGrid();
        }

        // ─── TABS ─────────────────────────────────────────────────────
        function switchTab(name) {
            currentTab = name;
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
                btn.classList.add('text-gray-300');
                btn.classList.remove('text-white');
            });
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            const btn = [...document.querySelectorAll('.tab-btn')].find(b => b.textContent.trim().includes(name === 'כולם' ? 'סקירה' : name));
            if (btn) { btn.classList.add('active'); btn.classList.remove('text-gray-300'); }
            const tab = document.getElementById('tab-' + name);
            if (tab) tab.classList.add('active');
        }

        // ─── MODAL ───────────────────────────────────────────────────
        function openAddTaskModal(mode) {
            modalMode = mode;
            const titles = { global: 'הוספת משימה לכל החטמ"רים', local: 'הוספת משימה אישית' };
            document.getElementById('modalTitle').textContent = titles[mode] || 'הוספת משימה לחטמ"ר ' + mode;
            document.getElementById('taskTitleInput').value = '';
            document.getElementById('taskDescInput').value = '';
            document.getElementById('taskUrgentInput').checked = false;
            document.getElementById('addTaskModal').classList.remove('hidden');
            document.getElementById('taskTitleInput').focus();
        }
        function closeModal() { document.getElementById('addTaskModal').classList.add('hidden'); }

        function submitTask() {
            const title = document.getElementById('taskTitleInput').value.trim();
            if (!title) { document.getElementById('taskTitleInput').focus(); return; }
            const task = {
                id: Date.now().toString(),
                title,
                desc: document.getElementById('taskDescInput').value.trim(),
                urgent: document.getElementById('taskUrgentInput').checked,
                category: ''
            };
            if (modalMode === 'global') {
                data.globalTasks.push(task);
                saveData();
                renderGlobalTaskListAdmin();
                renderOverviewGrid();
                BRIGADES.forEach(b => renderBrigadeTabForAdmin(b));
            } else if (modalMode === 'local') {
                if (!data.brigadeTasks[currentUser]) data.brigadeTasks[currentUser] = [];
                data.brigadeTasks[currentUser].push(task);
                saveData();
                renderLocalTaskList(currentUser);
                updateStats(currentUser);
            } else {
                // adding to specific brigade from admin
                if (!data.brigadeTasks[modalMode]) data.brigadeTasks[modalMode] = [];
                data.brigadeTasks[modalMode].push(task);
                saveData();
                renderBrigadeTabForAdmin(modalMode);
                renderOverviewGrid();
            }
            closeModal();
        }

        // ─── EXCEL EXPORT ────────────────────────────────────────────
        function exportToExcel() {
            const wb = XLSX.utils.book_new();
            // Global tasks sheet
            const globalRows = [['#', 'כותרת', 'פירוט', 'קטגוריה', 'חובת עדכון', ...BRIGADES.map(b => 'ביצוע - ' + b)]];
            data.globalTasks.forEach((t, i) => {
                const row = [i + 1, t.title, t.desc, t.category || '', t.urgent ? 'כן' : ''];
                BRIGADES.forEach(b => {
                    const comp = data.completions[b] || {};
                    row.push(comp['g_' + t.id] ? '✓' : '');
                });
                globalRows.push(row);
            });
            const ws1 = XLSX.utils.aoa_to_sheet(globalRows);
            ws1['!cols'] = [{ wch: 4 }, { wch: 35 }, { wch: 55 }, { wch: 10 }, { wch: 12 }, ...BRIGADES.map(() => ({ wch: 14 }))];
            ws1['!rtl'] = true;
            XLSX.utils.book_append_sheet(wb, ws1, 'משימות אוגדתיות');

            // Per brigade sheets
            BRIGADES.forEach(b => {
                const rows = [['#', 'כותרת', 'פירוט', 'חובת עדכון', 'בוצע']];
                const comp = data.completions[b] || {};
                data.globalTasks.forEach((t, i) => {
                    rows.push([i + 1, t.title, t.desc, t.urgent ? 'כן' : '', comp['g_' + t.id] ? '✓' : '']);
                });
                (data.brigadeTasks[b] || []).forEach((t, i) => {
                    rows.push([data.globalTasks.length + i + 1, t.title, t.desc, t.urgent ? 'כן' : '', comp['l_' + t.id] ? '✓' : '']);
                });
                const ws = XLSX.utils.aoa_to_sheet(rows);
                ws['!cols'] = [{ wch: 4 }, { wch: 35 }, { wch: 55 }, { wch: 12 }, { wch: 8 }];
                ws['!rtl'] = true;
                XLSX.utils.book_append_sheet(wb, ws, b);
            });

            XLSX.writeFile(wb, 'משימות_רבנות_פורים_פסח.xlsx');
        }

        // ─── KEYBOARD ────────────────────────────────────────────────
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') closeModal();
            if (e.key === 'Enter' && !document.getElementById('addTaskModal').classList.contains('hidden')) {
                if (e.target.tagName !== 'TEXTAREA') submitTask();
            }
        });

        // ─── INIT ─────────────────────────────────────────────────────
        loadData();
        const savedUser = localStorage.getItem('currentUser');
        if (savedUser) {
            login(savedUser);
        } else {
            document.getElementById('loginScreen').classList.remove('hidden');
        }
    </script>
</body>

</html>
