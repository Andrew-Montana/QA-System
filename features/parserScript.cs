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
            UseAdvancedParser();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("Done!");
            Console.ReadLine();
        }

        public static void UsePackage(string html)
        {
            var doc = new HtmlDocument();
            doc.LoadHtml(html);

            var query = from table in doc.DocumentNode.SelectNodes("//table").Cast<HtmlNode>()
                        from row in table.SelectNodes("tr").Cast<HtmlNode>()
                        from cell in row.SelectNodes("th|td").Cast<HtmlNode>()
                        select new { Table = table.Id, CellText = cell.InnerText };

            foreach (var cell in query)
            {
                Console.WriteLine("{0}: {1}", cell.Table, cell.CellText);
            }
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
                    mainList.Add(new Data() { keys = keys, values = values, info = info, titles = titles});

            }
            // delete existing files in folder before writing new
            string[] files = Directory.GetFiles(@"C:\Users\Ghost\Desktop\data\");
            int filesCount = files.Length;
            for (int i = 0; i < filesCount; i++)
            {
                File.Delete(files[i]);
            }
            // create files:
            for (int i = 0; i < mainList.Count; i++) 
            {
                if(mainList[i].keys.Count != 0)
                {
                    string s = "";
                    for (int j = 0; j < mainList[i].keys.Count; j++)
                    {
                            s += mainList[i].keys[j].Trim() + ";;;\t" + mainList[i].values[j].Trim() + ";;;\t" + mainList[i].info[j].ToString().Trim() + ";;;\n";
                    }

                    using (StreamWriter sw = new StreamWriter(@"C:\Users\Ghost\Desktop\data\" + mainList[i].keys[0].ToString().Trim() + ".csv", append: true))
                    {
                        sw.Write(s);
                    }
                }
            }
            // Console.WriteLine(mainList.Count);

        }

    /*    public static void UseSingleParser()
        {
            HtmlDocument doc = new HtmlDocument();
            doc.LoadHtml(GetTable1());
            var tableNode = doc.DocumentNode.SelectSingleNode("//table[1]");

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
            foreach (var list in table)
            {
                //enumerate the inner list
                foreach (var item in list)
                {
                    //output the actual item
                    if (!String.IsNullOrWhiteSpace(item))
                    {
                        if (counter == 0)
                            keys.Add(item);
                        if (counter == 1)
                            values.Add(item);
                        if (counter == 2)
                            info.Add(item);

                        counter++;

                        if (counter > 2)
                            counter = 0;
                    }
                }
            }
            //
            Console.WriteLine("##Keys##");
            Console.WriteLine(keys.Count);
            foreach (var key in keys)
            {
                Console.WriteLine(key);
            }
            Console.WriteLine("##Values##");
            Console.WriteLine(values.Count);
            foreach (var value in values)
            {
                Console.WriteLine(value);
            }
        }*/

        public static string GetCode()
        {
            string sourcecode = "";
            using (StreamReader sr = new StreamReader(@"c:\Users\Ghost\Desktop\mapfeatures.html"))
            {
                sourcecode = sr.ReadToEnd();
            }
            return sourcecode;
        }

        public static string GetTable1()
        {
            string sourcecode = "";
            using (StreamReader sr = new StreamReader(@"d://code_table1.txt"))
            {
                sourcecode = sr.ReadToEnd();
            }
            return sourcecode;
        }

    }
}
