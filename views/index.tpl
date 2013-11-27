% rebase layout route_prefix=route
<p>Notes</p>
<form action="/new">
      <input type="submit" value="New Note">
</form>
<table border="1">
%if new == True:
<form action="/new" method="POST">
<input type="text" size="100" maxlength="100" name="title">
<input type="text" size="100" maxlength="100" name="content">
<input type="submit" name="save" value="save">
</form>
%end
%for row in rows:
  <tr>
    <td>{{row.get('id')}}</td>
    <td>{{row.get('title')}}</td>
    <td>{{row.get('content')}}</td>
    <td><form action="/delete/{{row.get('id')}}">
              <input type="submit" value="Delete Note">
        </form>
    </td>
  </tr>
%end
</table>