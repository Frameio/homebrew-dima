class Dima < Formula
  include Language::Python::Virtualenv

  desc "CLI to view and kill running queries in postgres"
  homepage "https://github.com/Frameio/homebrew-dima"
  url "https://github.com/Frameio/homebrew-dima/raw/master/v1.0.0.tar.gz"
  sha256 "5806856f688a3adf959f4643991b53dc7baf28975f69d7866e4307798bdc7153"

  bottle :unneeded

  depends_on "postgresql"
  depends_on "python@2"

  resource "terminaltables" do
    url "https://files.pythonhosted.org/packages/9b/c4/4a21174f32f8a7e1104798c445dacdc1d4df86f2f26722767034e4de4bff/terminaltables-3.1.0.tar.gz"
    sha256 "f3eb0eb92e3833972ac36796293ca0906e998dc3be91fbe1f8615b331b853b81"
  end

  resource "psycopg2" do
    url "https://files.pythonhosted.org/packages/c0/07/93573b97ed61b6fb907c8439bf58f09957564cf7c39612cef36c547e68c6/psycopg2-2.7.6.1.tar.gz"
    sha256 "27959abe64ca1fc6d8cd11a71a1f421d8287831a3262bd4cacd43bbf43cc3c82"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"dima", "--help"
  end
end
