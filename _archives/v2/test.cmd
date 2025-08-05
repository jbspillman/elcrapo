1@ECHO OFF
ECHO.
ECHO.
ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES1 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES1 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES1 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES1 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES1 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES1 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES1.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES1 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES1.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES1 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES1 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES1.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES1 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES1 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES1.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES1 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES2 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES2 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES2 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES2 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES2 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES2 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES2.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES2 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES2.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES2 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES2 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES2.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES2 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES2 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES2.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES2 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES3 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES3 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES3 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES3 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES3 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES3 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES3.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES3 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES3.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES3 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES3 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES3.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES3 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES3 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES3.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES3 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES4 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES4 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES4 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES4 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES4 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES4 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES4.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES4 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES4.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES4 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES4 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES4.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES4 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES4 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES4.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES4 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES5 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES5 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES5 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES5 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES5 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5 : /bench/nfs3_032k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES5 /bench/nfs3_032k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Write_Large_Files__T4.[D2xF8].B1M.S1G.D1.S1_NODES5.txt"  --write --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --sync --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label SWLF__T4.[D2xF8].B1M.S1G.D1.S1_NODES5 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Sequential_Read_Large_Files__T4.[D2xF8].B1M.S1G.D1.S0_NODES5.txt" --read --trunctosize --threads=4 --dirs=2 --files=8 --block=1M --size=1G --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label SRLF__T4.[D2xF8].B1M.S1G.D1.S0_NODES5 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Write_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.txt" --write --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --deldirs --delfiles --cpu --lat --lathisto --label RWSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES5 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Random_Read_SmallBlocks__T8.[D4xF16].B4K.S512M.D1.S0_NODES5.txt" --read --rand --trunctosize --threads=8 --dirs=4 --files=16 --block=4K --size=512M --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label RRSB__T8.[D4xF16].B4K.S512M.D1.S0_NODES5 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_70Read_30Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=70 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR70W30__T6.[D3xF12].B64K.S256M.D1.S0_NODES5 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


ECHO "Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5 : /bench/nfs3_128k/io_data" 
"C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_client\elbencho.exe" --hosts "mediaserver.beastmode.local.net,centos01.beastmode.local.net,centos02.beastmode.local.net,centos03.beastmode.local.net,centos04.beastmode.local.net" --live1 --livecsv "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5_LIVE.csv" --csvfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.csv"  --jsonfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.json"  --resfile "C:\Users\spillman\PythonProjects\PY_ELBENCHO\elbencho_results\Mixed_30Read_70Write__T6.[D3xF12].B64K.S256M.D1.S0_NODES5.txt" --write --rand --threads=6 --dirs=3 --files=12 --block=64K --size=256M --rwmixpct=30 --direct --timelimit 120 --mkdirs --nodelerr --cpu --lat --lathisto --label MR30W70__T6.[D3xF12].B64K.S256M.D1.S0_NODES5 /bench/nfs3_128k/io_data
timeout /t 3 /nobreak 
ECHO.
ECHO.


