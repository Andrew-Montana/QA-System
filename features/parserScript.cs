using HtmlAgilityPack;
using System;
using System.IO;
using System.Net;
using System.Collections.Generic;
using System.Linq;

// id="Aerialway"
// 290 line
//

namespace parseMF
{
    class Program
    {
        private static string[] mainKeys = {"aerialway","aeroway","amenity","barrier","boundary","building","craft","emergency","geological","highway","historic","landuse","leisure","man_made","military","natural","office","place","power","public_transport","railway","route","shop","sport","telecom","tourism","waterway"};

        static void Main(string[] args)
        {
             //UseAdvancedParser();
            // MyConsole.Print("Done!", ConsoleColor.Green);
            //ChangeData();
            Console.ReadLine();
        }

        private static void ChangeData()
        {
            List<string> listA = new List<string>();
            List<string> listB = new List<string>();

            MyConsole.Print("Changing data...");
            // Read main data file
            using (var reader = new StreamReader(@"C:\Users\Ghost\Desktop\data\all_data\data.csv"))
            {
                while (!reader.EndOfStream)
                {
                    var line = reader.ReadLine();
                    if(!string.IsNullOrEmpty(line))
                    {
                        var values = line.Split(";;;");

                        // make spaces
                        if(values[1].Contains('_') || values[1].Contains('-'))
                        {
                            values[1] = values[1].Contains('_') == true ? values[1].Replace('_', ' ') : values[1];
                            values[1] = values[1].Contains('-') == true ? values[1].Replace('-', ' ') : values[1];
                            MyConsole.Print("-/_ have been changed", ConsoleColor.DarkYellow);
                        }
                        // get rid of 'yes' strings
                        if (values[1] != "yes")
                        {
                            listA.Add(values[0]);
                            listB.Add(values[1]);
                        }
                        else
                        {
                            MyConsole.Print("'yes' string are deleted", ConsoleColor.DarkYellow);
                        }
                    }
                }
            }
            // make new file
            MyConsole.Print("File created!",ConsoleColor.Green);
            StreamWriter writer = new StreamWriter(@"C:\Users\Ghost\Desktop\data\all_data\newData.csv");
            for (int i = 0; i < listA.Count; i++)
            {
                writer.WriteLine(listA[i].ToString() + ";" + listB[i].ToString() + ";");
            }
            writer.Close();
            Console.ReadLine();
          
        }

        public static void UseAdvancedParser()
        {
            HtmlDocument doc = new HtmlDocument();
            doc.LoadHtml(GetCode());
            //
            var tableNodes = doc.DocumentNode.SelectNodes("//table");

            List<Data> mainList = new List<Data>();
            foreach (var tableNode in tableNodes)
            {
                var titles = tableNode.Descendants("th")
                                .Select(th => th.InnerText)
                                .ToList();

                var table = tableNode.Descendants("tr").Skip(1)
                                    .Select(tr => tr.Descendants("td")
                                                    .Select(td => td.InnerText)
                                                    .ToList())
                                    .ToList();
                int counter = 0;
                List<string> keys = new List<string>();
                List<string> values = new List<string>();
                List<string> info = new List<string>();
                //enumerate all lists in the outer list
                foreach (var list in table) // list - string. table - table
                {
                    //enumerate the inner list
                    foreach (var item in list) // list - строка. item - значения/столбцы
                    {
                        // restriction key must equal to the name of category/prepared keys
                        if (counter == 0)
                            if (!mainKeys.Contains(item.Trim().ToString()))
                                break;
                        //
                        bool firstIf = false;

                            if(titles.Count >= 7)
                            {
                                #region pattern 1
                                // Aeroway i.e.
                                if (titles[3].Trim() == "Description" && titles[4].Trim() == "Map rendering" && titles[5].Trim() == "Image" && titles[6].Trim() == "Count")
                                {
                                    if (counter == 0)
                                        keys.Add(item.Trim());
                                    if (counter == 1)
                                        values.Add(item.Trim());
                                    if (counter == 3)
                                    {
                                        info.Add(item.Trim());
                                    }

                                    counter++;
                                firstIf = true;
                                }
                                #endregion
                                #region pattern 2
                                // Aeroway i.e.
                                else if (titles[3].Trim() == "Description" && titles[4].Trim() == "Map rendering" && titles[5].Trim() == "Image" && titles[6].Trim() == "Count")
                                {
                                    if (counter == 0)
                                        keys.Add(item.Trim());
                                    if (counter == 1)
                                        values.Add(item.Trim());
                                    if (counter == 3)
                                        info.Add(item.Trim());

                                    counter++;
                                firstIf = true;
                                }
                                #endregion
                            }
                            if (titles.Count >= 6 && firstIf == false)
                            {
                                #region pattern 3 (i.e. power)
                                if (titles[2].Trim() == "Element" && titles[3].Trim() == "Comment" && titles[4].Trim() == "Rendering" && titles[5].Trim() == "Photo")
                                {
                                    if (counter == 0)
                                        keys.Add(item.Trim());
                                    if (counter == 1)
                                        values.Add(item.Trim());
                                    if (counter == 3)
                                        info.Add(item.Trim());

                                    counter++;
                                }
                                #endregion
                                #region pattern 4
                                else if (titles[2].Trim() == "Element" && titles[3].Trim() == "Comment" && titles[4].Trim() == "Rendering carto" && titles[5].Trim() == "Photo")
                                {

                                    if (counter == 0)
                                        keys.Add(item.Trim());
                                    if (counter == 1)
                                        values.Add(item.Trim());
                                    if (counter == 3)
                                        info.Add(item.Trim());

                                    counter++;
                                }
                                #endregion
                                #region pattern 5
                                else if (titles[2].Trim() == "Element" && titles[3].Trim() == "Comment" && titles[4].Trim() == "carto-Rendering" && titles[5].Trim() == "Photo")
                                {
                                    if (counter == 0)
                                        keys.Add(item.Trim());
                                    if (counter == 1)
                                        values.Add(item.Trim());
                                    if (counter == 3)
                                        info.Add(item.Trim());

                                    counter++;
                                }
                                #endregion
                                #region pattern 6
                                else if (titles[2].Trim() == "Element" && titles[3].Trim() == "Comment" && titles[4].Trim() == "Rendering example" && titles[5].Trim() == "Photo")
                                {
                                    if (counter == 0)
                                        keys.Add(item.Trim());
                                    if (counter == 1)
                                        values.Add(item.Trim());
                                    if (counter == 3)
                                        info.Add(item.Trim());

                                    counter++;
                                }
                            #endregion
                            #region pattern 7
                            else if (titles[2].Trim() == "Element" && titles[3].Trim() == "Comment" && titles[4].Trim() == "Rendering on default layer (osm-carto)" && titles[5].Trim() == "Photo")
                            {

                                if (counter == 0)
                                    keys.Add(item.Trim());
                                if (counter == 1)
                                    values.Add(item.Trim());
                                if (counter == 3)
                                    info.Add(item.Trim());

                                counter++;
                            }

                            #endregion
                            #region pattern 8
                            else if (titles[2].Trim() == "Element" && titles[3].Trim() == "Comment" && titles[4].Trim() == "Photo")
                            {

                                if (counter == 0)
                                    keys.Add(item.Trim());
                                if (counter == 1)
                                    values.Add(item.Trim());
                                if (counter == 3)
                                    info.Add(item.Trim());

                                counter++;
                            }
                            else if (titles[2].Trim() == "Element" && titles[3].Trim() == "Description" && titles[4].Trim() == "Rendering" && titles[5].Trim() == "Photo")
                            {

                                if (counter == 0)
                                    keys.Add(item.Trim());
                                if (counter == 1)
                                    values.Add(item.Trim());
                                if (counter == 3)
                                    info.Add(item.Trim());

                                counter++;
                            }
                            else if (titles[2].Trim() == "Element" && titles[3].Trim() == "Description" && titles[4].Trim() == "Map rendering" && titles[5].Trim() == "Image")
                            {

                                if (counter == 0)
                                    keys.Add(item.Trim());
                                if (counter == 1)
                                    values.Add(item.Trim());
                                if (counter == 3)
                                    info.Add(item.Trim());

                                counter++;
                            }
                            else if (titles[2].Trim() == "Element" && titles[3].Trim() == "Description" && titles[4].Trim() == "Image" && titles[5].Trim() == "Count")
                            {

                                if (counter == 0)
                                    keys.Add(item.Trim());
                                if (counter == 1)
                                    values.Add(item.Trim());
                                if (counter == 3)
                                    info.Add(item.Trim());

                                counter++;
                            }

                            #endregion
                        }


                    }
                    counter = 0;
                }
                if(keys.Count > 0)
                    mainList.Add(new Data() { keys = keys, values = values, titles = titles}); // info = info, 

            }
            // delete existing files in folder before writing new
            string[] files = Directory.GetFiles(@"C:\Users\Ghost\Desktop\data\");
            int filesCount = files.Length;
            for (int i = 0; i < filesCount; i++)
            {
                File.Delete(files[i]);
            }
            // create files:
            string allIn = "";
            for (int i = 0; i < mainList.Count; i++) 
            {
                if(mainList[i].keys.Count != 0)
                {
                    string s = "";
                    for (int j = 0; j < mainList[i].keys.Count; j++)
                    {
                        // s += mainList[i].keys[j].Trim() + ";;;\t" + mainList[i].values[j].Trim() + ";;;\t" + mainList[i].info[j].ToString().Trim() + ";;;\n";
                        s += mainList[i].keys[j].Trim() + ";;;" + mainList[i].values[j].Trim() + ";;;\n";
                    }

                    using (StreamWriter sw = new StreamWriter(@"C:\Users\Ghost\Desktop\data\" + mainList[i].keys[0].ToString().Trim() + ".csv", append: true))
                    {
                        sw.Write(s);
                    }
                    allIn += s + "\n";
                }
            }
            if(!Directory.Exists(@"C:\Users\Ghost\Desktop\data\all_data\"))
            {
                Directory.CreateDirectory(@"C:\Users\Ghost\Desktop\data\all_data\");
            }
            StreamWriter streamWriter = new StreamWriter(@"C:\Users\Ghost\Desktop\data\all_data\data.csv");
            streamWriter.Write(allIn);
            streamWriter.Close();

        }

        public static string GetCode()
        {
            string sourcecode = "";
            using (StreamReader sr = new StreamReader(@"c:\Users\Ghost\Desktop\mapfeatures.html"))
            {
                sourcecode = sr.ReadToEnd();
            }
            return sourcecode;
        }

    }
}
